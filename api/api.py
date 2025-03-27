from fastapi import FastAPI, HTTPException, Depends
from db.database import DatabaseManager
from config import DB_PATH

app=FastAPI(title="GPU Monitoring API",version="1.0")

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
    return state