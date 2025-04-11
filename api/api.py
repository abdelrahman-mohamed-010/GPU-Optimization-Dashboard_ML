from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from db.database import DatabaseManager
from config import DB_PATH

app=FastAPI(title="GPU Monitoring API",version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db_manager=DatabaseManager()
    db_manager.connect()
    try:
        yield db_manager
    finally:
        db_manager.close()


@app.get("/gpus/{gpu_id}")
def get_gpu_state(gpu_id: str, db_manager: DatabaseManager = Depends(get_db)):
    state = db_manager.get_gpu_state(gpu_id)
    if state['static'] is None:
        raise HTTPException(status_code=404, detail=f"GPU not found against GPU id: {gpu_id}")
    return {"static": state["static"], "dynamic": state["dynamic"]}


@app.get("/overview_stats")
def overview_stats(db_manager: DatabaseManager = Depends(get_db)):
    cursor = db_manager.conn.cursor()
    
    # Total number of GPUs
    total_gpus = cursor.execute("SELECT COUNT(*) FROM gpu_static").fetchone()[0]
    
    # Count GPUs per company
    static_records = cursor.execute("SELECT model FROM gpu_static").fetchall()
    companies = {"NVIDIA": 0, "AMD": 0, "INTEL": 0}
    for (model,) in static_records:
        company = "NVIDIA"
        companies[company] = companies.get(company, 0) + 1
    
    # Aggregate dynamic stats: average utilization and average power consumption.
    agg_query = """
    SELECT AVG(t.utilization) as avg_util, AVG(t.power_w) as avg_power
    FROM gpu_dynamic t
    INNER JOIN (
        SELECT id, MAX(timestamp) as max_ts
        FROM gpu_dynamic
        GROUP BY id
    ) tm ON t.id = tm.id AND t.timestamp = tm.max_ts
    """
    result = cursor.execute(agg_query).fetchone()
    avg_util = result[0] if result[0] is not None else 0
    avg_power = result[1] if result[1] is not None else 0
    power_efficiency = avg_util / avg_power if avg_power > 0 else 0

    return {
        "total_gpus": total_gpus,
        "companies": companies,
        "average_utilization": int(avg_util),
        "power_efficiency": int(power_efficiency*100)
    }