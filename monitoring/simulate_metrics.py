import random
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from db.database import DatabaseManager
from config import MONITOR_INTERVAL, NUM_WORKERS

def load_gpu_list():
    """
    Returns a list of GPUs with additional cluster information.
    Each record is a tuple: (gpu_id, model, memory_total_gb, cluster_name)
    """
    db = DatabaseManager()
    db.connect()
    cur = db.conn.cursor()
    # Join gpus with racks to get the cluster name.
    cur.execute("""
        SELECT g.gpu_id, g.model, g.memory_total_gb, r.cluster_name
        FROM gpus g
        JOIN racks r ON g.rack_id = r.rack_id
    """)
    gpu_list = cur.fetchall()
    db.close()
    return gpu_list

def chunkify(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def process_gpu_chunk(chunk):
    """
    For each GPU record, simulate one metrics insertion.
    The simulation uses a baseline computed from the cluster name
    to yield different average utilizations across clusters.
    """
    db = DatabaseManager()
    db.connect()
    cur = db.conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for gpu in chunk:
        gpu_id, model, mem_total, cluster_name = gpu
        # Compute a baseline utilization for this GPU's cluster.
        # This yields a baseline in the range [30, 100]
        baseline = (abs(hash(cluster_name)) % 71) + 30  
        # Generate a utilization with Gaussian noise around the baseline.
        utilization = random.gauss(baseline, 10)
        utilization = max(0, min(utilization, 100))
        # Determine temperature based on utilization.
        if utilization < 40:
            temperature = random.uniform(30, 50)
        elif utilization < 70:
            temperature = random.uniform(50, 70)
        else:
            temperature = random.uniform(70, 95)
        # Simulate memory used proportional to utilization, with some noise.
        memory_used = (utilization / 100) * mem_total * random.uniform(0.9, 1.1)
        # Determine power based on utilization.
        if utilization < 40:
            power = random.uniform(50, 150)
        elif utilization < 70:
            power = random.uniform(150, 300)
        else:
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
                future.result()  # Wait for all threads to finish.
        print(f"Inserted metrics for {len(gpu_list)} GPUs at {datetime.datetime.now()}")
        time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    simulate_gpu_metrics()
