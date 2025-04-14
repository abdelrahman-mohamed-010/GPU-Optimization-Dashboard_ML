from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from db.database import DatabaseManager
from config import DB_PATH
import random

app = FastAPI(title="Datacenter API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


def get_db():
    db_manager = DatabaseManager(db_path=DB_PATH)
    db_manager.connect()
    try:
        yield db_manager
    finally:
        db_manager.close()

@app.get("/gpus/{gpu_id}")
def get_gpu_details(gpu_id: str, db: DatabaseManager = Depends(get_db)):
    cur = db.conn.cursor()
    cur.execute("""
        SELECT gpu_id, rack_id, vendor, model, memory_total_gb, compute_tflops, bandwidth_gbps 
        FROM gpus 
        WHERE gpu_id = ?
    """, (gpu_id,))
    static_info = cur.fetchone()
    if static_info is None:
        raise HTTPException(status_code=404, detail="GPU not found")
    cur.execute("""
        SELECT utilization, memory_used_gb, temperature, power_watts, timestamp 
        FROM gpu_metrics 
        WHERE gpu_id = ? 
          AND timestamp = (SELECT MAX(timestamp) FROM gpu_metrics WHERE gpu_id = ?)
    """, (gpu_id, gpu_id))
    dynamic_info = cur.fetchone()
    return {"static": static_info, "dynamic": dynamic_info}

@app.get("/clusters")
def list_clusters(db: DatabaseManager = Depends(get_db)):
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM clusters")
    clusters = cur.fetchall()
    return {"clusters": clusters}

@app.get("/clusters/{cluster_name}/racks")
def list_racks(cluster_name: str, db: DatabaseManager = Depends(get_db)):
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM racks WHERE cluster_name = ?", (cluster_name,))
    racks = cur.fetchall()
    return {"racks": racks}

@app.get("/racks/{rack_id}/gpus")
def list_gpus_in_rack(rack_id: str, db: DatabaseManager = Depends(get_db)):
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM gpus WHERE rack_id = ?", (rack_id,))
    gpus = cur.fetchall()
    return {"gpus": gpus}

@app.get("/cluster_overview")
def cluster_overview(db: DatabaseManager = Depends(get_db)):
    """
    Returns a health overview for each cluster using the latest metric entry per GPU.
    Only 4 random clusters are returned.
    """
    cur = db.conn.cursor()
    query = """
        SELECT c.cluster_name, AVG(gm.utilization) as avg_util, AVG(gm.temperature) as avg_temp, 
               SUM(CASE WHEN gm.utilization >= 95 THEN 1 ELSE 0 END) as alerts
        FROM clusters c
        JOIN racks r ON c.cluster_name = r.cluster_name
        JOIN gpus g ON r.rack_id = g.rack_id
        JOIN (
            SELECT gpu_id, utilization, temperature, timestamp
            FROM gpu_metrics
            WHERE (gpu_id, timestamp) IN (
                SELECT gpu_id, MAX(timestamp)
                FROM gpu_metrics
                GROUP BY gpu_id
            )
        ) gm ON g.gpu_id = gm.gpu_id
        GROUP BY c.cluster_name
    """
    rows = cur.execute(query).fetchall()
    cluster_overview = []
    for cluster_name, avg_util, avg_temp, alerts in rows:
        if avg_util < 90:
            status = "Healthy"
        elif avg_util < 95:
            status = "Warning"
        else:
            status = "Critical"
        if avg_temp < 60:
            temp_class = "Normal"
        elif avg_temp < 80:
            temp_class = "High"
        else:
            temp_class = "Critical"
        cluster_overview.append({
            "cluster_name": cluster_name,
            "status": status,
            "current_utilization": round(avg_util, 2),
            "current_temperature": temp_class,
            "alerts": "None" if alerts == 0 else f"{alerts} active"
        })
    # Return only 4 random clusters
    if len(cluster_overview) > 4:
        cluster_overview = random.sample(cluster_overview, 4)
    return {"cluster_overview": cluster_overview}

@app.get("/overview")
def overview(db: DatabaseManager = Depends(get_db)):
    """
    Provides an overall dashboard view including:
      - Total GPUs
      - Average utilization (using the latest metric for each GPU)
      - Average power efficiency, computed as (avg utilization / avg power) * 100,
        based on the latest metric for each GPU.
      - GPU counts by vendor
      - Cluster health overview (4 random clusters)
    """
    cur = db.conn.cursor()
    
    # Total GPUs.
    total_gpus = cur.execute("SELECT COUNT(*) FROM gpus").fetchone()[0]
    
    # Compute average utilization and average power using the latest record per GPU.
    agg_query = """
        SELECT AVG(gm.utilization) as avg_util, AVG(gm.power_watts) as avg_power
        FROM gpu_metrics gm
        WHERE (gm.gpu_id, gm.timestamp) IN (
            SELECT gpu_id, MAX(timestamp)
            FROM gpu_metrics
            GROUP BY gpu_id
        )
    """
    agg = cur.execute(agg_query).fetchone()
    avg_util = agg[0] if agg[0] is not None else 0
    avg_power = agg[1] if agg[1] is not None else 0
    power_efficiency = (avg_util / avg_power * 100) if avg_power > 0 else 0
    
    # GPU counts by vendor.
    vendor_counts = {}
    rows = cur.execute("SELECT vendor, COUNT(*) FROM gpus GROUP BY vendor").fetchall()
    for vendor, count in rows:
        vendor_counts[vendor] = count

    # Get cluster health overview as in /cluster_overview.
    cluster_query = """
        SELECT c.cluster_name, AVG(gm.utilization) as avg_util, AVG(gm.temperature) as avg_temp, 
               SUM(CASE WHEN gm.utilization >= 95 THEN 1 ELSE 0 END) as alerts
        FROM clusters c
        JOIN racks r ON c.cluster_name = r.cluster_name
        JOIN gpus g ON r.rack_id = g.rack_id
        JOIN (
            SELECT gpu_id, utilization, temperature, timestamp
            FROM gpu_metrics
            WHERE (gpu_id, timestamp) IN (
                SELECT gpu_id, MAX(timestamp)
                FROM gpu_metrics
                GROUP BY gpu_id
            )
        ) gm ON g.gpu_id = gm.gpu_id
        GROUP BY c.cluster_name
    """
    clusters = []
    for row in cur.execute(cluster_query).fetchall():
        cluster_name, avg_util_cluster, avg_temp, alerts = row
        if avg_util_cluster < 90:
            status = "Healthy"
        elif avg_util_cluster < 95:
            status = "Warning"
        else:
            status = "Critical"
        if avg_temp < 60:
            temp_class = "Normal"
        elif avg_temp < 80:
            temp_class = "High"
        else:
            temp_class = "Critical"
        clusters.append({
            "cluster_name": cluster_name,
            "status": status,
            "current_utilization": round(avg_util_cluster, 2),
            "current_temperature": temp_class,
            "alerts": "None" if alerts == 0 else f"{alerts} active"
        })
    if len(clusters) > 4:
        clusters = random.sample(clusters, 4)
    
    return {
        "total_gpus": total_gpus,
        "avg_utilization": round(avg_util, 2),
        "avg_power_efficiency": round(power_efficiency, 2),
        "vendor_counts": vendor_counts,
        "cluster_health": clusters
    }

@app.get("/rl_performance")
def get_rl_performance(db: DatabaseManager = Depends(get_db)):
    """
    Retrieve the stored Federated PPO RL performance data from the database.
    Returns performance data for each day.
    """
    cur = db.conn.cursor()
    cur.execute("SELECT day, average_reward, timestamp FROM rl_performance ORDER BY performance_id ASC")
    records = cur.fetchall()
    results = [{"day": r[0], "average_reward": r[1], "timestamp": r[2]} for r in records]
    return {"rl_performance": results}
