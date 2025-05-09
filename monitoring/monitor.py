import random
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from db.database import DatabaseManager
from config import MONITOR_INTERVAL, NUM_WORKERS

def load_gpu_list():
    db = DatabaseManager()
    db.connect()
    gpu_list = db.get_all_gpus()  # Returns list of (gpu_id, model, memory_total_gb)
    db.close()
    return gpu_list

def chunkify(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def process_gpu_chunk(chunk):
    db = DatabaseManager()
    db.connect()
    cur = db.conn.cursor()
    now = datetime.datetime.now()
    for gpu in chunk:
        gpu_id, model, mem_total = gpu
        category = random.choices(['low', 'medium', 'high'], weights=[0.4, 0.4, 0.2])[0]
        if category == 'low':
            utilization = random.uniform(0, 30)
            temperature = random.uniform(30, 50)
            memory_used = random.uniform(0, 0.3 * mem_total)
            power = random.uniform(50, 150)
        elif category == 'medium':
            utilization = random.uniform(30, 70)
            temperature = random.uniform(50, 70)
            memory_used = random.uniform(0.3 * mem_total, 0.7 * mem_total)
            power = random.uniform(150, 300)
        else:
            utilization = random.uniform(70, 100)
            temperature = random.uniform(70, 95)
            memory_used = random.uniform(0.7 * mem_total, mem_total)
            power = random.uniform(300, 500)
        cur.execute("""
            INSERT INTO gpu_metrics (gpu_id, utilization, memory_used_gb, temperature, power_watts, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (gpu_id, utilization, memory_used, temperature, power, now))
    db.conn.commit()
    db.close()

def simulate_gpu_metrics():
    gpu_list = load_gpu_list()
    num_workers = NUM_WORKERS
    chunk_size = len(gpu_list) // num_workers
    if len(gpu_list) % num_workers != 0:
        chunk_size += 1
    while True:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            chunks = list(chunkify(gpu_list, chunk_size))
            futures = [executor.submit(process_gpu_chunk, chunk) for chunk in chunks]
            for future in futures:
                future.result()
        print(f"Inserted metrics for {len(gpu_list)} GPUs at {datetime.datetime.now()}")
        time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    simulate_gpu_metrics()
