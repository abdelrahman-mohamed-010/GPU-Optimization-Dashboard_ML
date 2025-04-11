# monitoring/monitor.py

import asyncio
import random
from datetime import datetime
from db.database import DatabaseManager
from config import MONITOR_INTERVAL

async def monitor_gpus(monitor_interval=MONITOR_INTERVAL):
    db = DatabaseManager()
    db.connect()
    try:
        cursor = db.conn.cursor()
        static_data = cursor.execute("SELECT id, memory_total_gb FROM gpu_static").fetchall()
        gpu_info = {row[0]: row[1] for row in static_data} 
        gpu_ids = list(gpu_info.keys())
        while True:
            for gpu_id in gpu_ids:
                total_memory = gpu_info[gpu_id]  
                utilization = round(random.uniform(0, 100), 2)
                if utilization < 20:
                    memory_used = round(random.uniform(0.05 * total_memory, 0.3 * total_memory), 2)
                elif utilization < 60:
                    memory_used = round(random.uniform(0.3 * total_memory, 0.7 * total_memory), 2)
                else:
                    memory_used = round(random.uniform(0.7 * total_memory, total_memory), 2)
                if utilization < 20:
                    temperature = round(random.uniform(30, 50), 2)
                elif utilization < 60:
                    temperature = round(random.uniform(50, 70), 2)
                else:
                    temperature = round(random.uniform(70, 90), 2)
                if utilization < 20:
                    power_w = round(random.uniform(50, 150), 2)
                elif utilization < 60:
                    power_w = round(random.uniform(150, 250), 2)
                else:
                    power_w = round(random.uniform(250, 400), 2)
                dynamic_data = {
                    "utilization": utilization,
                    "memory_used_gb": memory_used,
                    "temperature": temperature,
                    "power_w": power_w
                }
                db.insert_gpu_dynamic(gpu_id, dynamic_data)
            print(f"[{datetime.now()}] Monitoring update: Updated dynamic metrics for {len(gpu_ids)} GPUs.")
            await asyncio.sleep(monitor_interval)
    except asyncio.CancelledError:
        print("Monitoring cancelled.")
    finally:
        db.close()

def start_monitoring():
    asyncio.run(monitor_gpus())
