from fastapi import FastAPI, HTTPException, Depends
from db.database import DatabaseManager
from config import DB_PATH

app = FastAPI(title="Datacenter API", version="1.0")

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
        ORDER BY timestamp DESC 
        LIMIT 1
    """, (gpu_id,))
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
    
    cur = db.conn.cursor()
    query = """
        SELECT c.cluster_name, gm.utilization, gm.temperature
        FROM clusters c
        JOIN racks r ON c.cluster_name = r.cluster_name
        JOIN gpus g ON r.rack_id = g.rack_id
        JOIN (
            SELECT gpu_id, MAX(timestamp) as latest_ts
            FROM gpu_metrics
            GROUP BY gpu_id
        ) sub ON g.gpu_id = sub.gpu_id
        JOIN gpu_metrics gm ON gm.gpu_id = sub.gpu_id AND gm.timestamp = sub.latest_ts
    """
    rows = cur.execute(query).fetchall()
    
    # Group results by cluster_name.
    cluster_data = {}
    for cluster_name, utilization, temperature in rows:
        if cluster_name not in cluster_data:
            cluster_data[cluster_name] = {
                "total": 0,
                "util_sum": 0.0,
                "temp_sum": 0.0,
                "alerts": 0
            }
        cluster_data[cluster_name]["total"] += 1
        cluster_data[cluster_name]["util_sum"] += utilization
        cluster_data[cluster_name]["temp_sum"] += temperature
        if utilization >= 95:
            cluster_data[cluster_name]["alerts"] += 1
    
    result = []
    for cluster_name, data in cluster_data.items():
        total = data["total"]
        avg_util = data["util_sum"] / total if total > 0 else 0
        avg_temp = data["temp_sum"] / total if total > 0 else 0
        alerts = data["alerts"]
        
        # Determine status based on average utilization.
        if avg_util < 90:
            status = "Healthy"
        elif avg_util < 95:
            status = "Warning"
        else:
            status = "Critical"
        
        # Determine temperature classification.
        if avg_temp < 60:
            temp_class = "Normal"
        elif avg_temp < 80:
            temp_class = "High"
        else:
            temp_class = "Critical"
        
        result.append({
            "cluster_name": cluster_name,
            "status": status,
            "average_utilization": round(avg_util, 2),
            "temperature": temp_class,
            "alerts": "None" if alerts == 0 else f"{alerts} active"
        })
        
    return {"clusters": result}
