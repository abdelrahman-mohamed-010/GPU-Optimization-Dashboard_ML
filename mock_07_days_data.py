import datetime
import random
from concurrent.futures import ThreadPoolExecutor
from db.database import DatabaseManager
from config import MONITOR_INTERVAL, NUM_WORKERS

# Total intervals for 7 days with 20 sec difference:
# 7 days * 24 * 60 * 60 / 20 = 30240 intervals per GPU
TOTAL_INTERVALS = 30240  

# Batch size for each GPU simulation
BATCH_SIZE = 1000

# Automatically set the start date to 40 days back from now.
START_DATE = datetime.datetime.now() - datetime.timedelta(days=7)

def simulate_metrics_for_gpu(gpu):
    """
    Given a GPU record (gpu_id, model, memory_total_gb, cluster_name),
    simulate its metrics over 7 days (each interval is 20 seconds)
    and insert into the gpu_metrics table in batches.
    """
    # Expecting a 4-tuple: (gpu_id, model, memory_total_gb, cluster_name)
    gpu_id, model, mem_total, cluster_name = gpu
    db = DatabaseManager()
    db.connect()
    
    # Compute a baseline utilization based on the cluster name to create variation.
    # This baseline is in the range [20, 90]
    baseline = (abs(hash(cluster_name)) % 71) + 20
    
    for i in range(0, TOTAL_INTERVALS, BATCH_SIZE):
        batch = []
        for j in range(i, min(i + BATCH_SIZE, TOTAL_INTERVALS)):
            # Calculate the timestamp for this interval.
            timestamp = START_DATE + datetime.timedelta(seconds=20 * j)
            # Generate a utilization using Gaussian noise around the baseline.
            utilization = random.gauss(baseline, 10)
            utilization = max(0, min(utilization, 100))
            
            # Temperature: lower at low utilization, higher at high.
            if utilization < 40:
                temperature = random.uniform(30, 50)
            elif utilization < 70:
                temperature = random.uniform(50, 70)
            else:
                temperature = random.uniform(70, 95)
            
            # Memory used is roughly proportional to utilization (with some noise).
            memory_used = (utilization / 100) * mem_total * random.uniform(0.9, 1.1)
            
            # Power consumption: lower for lower utilization, higher otherwise.
            if utilization < 40:
                power = random.uniform(50, 150)
            elif utilization < 70:
                power = random.uniform(150, 300)
            else:
                power = random.uniform(300, 500)
                
            batch.append((
                gpu_id,
                utilization,
                memory_used,
                temperature,
                power,
                timestamp.strftime("%Y-%m-%d %H:%M:%S")
            ))
        db.insert_gpu_metrics_batch(batch)
        if (i // BATCH_SIZE) % 100 == 0:
            print(f"GPU {gpu_id}: inserted {(i + len(batch))} out of {TOTAL_INTERVALS} intervals.")
    db.close()

def main():
    db = DatabaseManager()
    db.connect()
    cur = db.conn.cursor()
    # Load all GPUs along with the cluster name (join gpus with racks).
    cur.execute("""
        SELECT g.gpu_id, g.model, g.memory_total_gb, r.cluster_name
        FROM gpus g
        JOIN racks r ON g.rack_id = r.rack_id
    """)
    gpu_list = cur.fetchall()  # Each record: (gpu_id, model, memory_total_gb, cluster_name)
    db.close()
    print(f"Simulating 7 days of data (starting 7 days ago) for {len(gpu_list)} GPUs (20 sec intervals).")
    
    max_workers = NUM_WORKERS
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(simulate_metrics_for_gpu, gpu) for gpu in gpu_list]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
