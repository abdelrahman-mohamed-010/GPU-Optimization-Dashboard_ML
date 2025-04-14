import datetime
import random
import time
from concurrent.futures import ThreadPoolExecutor
from db.database import DatabaseManager
from config import MONITOR_INTERVAL, NUM_WORKERS

# TOTAL_INTERVALS for 2 days with 20 sec difference:
# 2 days * 24 * 60 * 60 / 20 = 8640 intervals per GPU
TOTAL_INTERVALS = 8640  

# Batch size for each GPU simulation
BATCH_SIZE = 1000

# Automatically set the start date (for simulation) to 2 days back from now.
START_DATE = datetime.datetime.now() - datetime.timedelta(days=2)

def load_gpu_list():
    """
    Load all GPUs along with the cluster name by joining gpus with racks.
    Returns a list of tuples: (gpu_id, model, memory_total_gb, cluster_name)
    """
    db = DatabaseManager()
    db.connect()
    cur = db.conn.cursor()
    cur.execute("""
        SELECT g.gpu_id, g.model, g.memory_total_gb, r.cluster_name
        FROM gpus g
        JOIN racks r ON g.rack_id = r.rack_id
    """)
    rows = cur.fetchall()
    # Ensure each row has exactly 4 elements.
    fixed_rows = []
    for row in rows:
        if len(row) == 4:
            fixed_rows.append(row)
        elif len(row) < 4:
            fixed_rows.append(row + ("",))
        else:
            fixed_rows.append(row[:4])
    db.close()
    return fixed_rows

def simulate_metrics_for_gpu(gpu):
    """
    Given a GPU record (gpu_id, model, memory_total_gb, cluster_name),
    simulate its metrics over 2 days (each interval is 20 seconds)
    and insert the records into the gpu_metrics table in batches.
    """
    # Unpack the GPU tuple (expected length: 4)
    gpu_id, model, mem_total, cluster_name = gpu
    db = DatabaseManager()
    db.connect()
    
    # Compute a baseline utilization based on the cluster name to create variation.
    baseline = (abs(hash(cluster_name)) % 71) + 20  # baseline in [20, 90]
    
    for i in range(0, TOTAL_INTERVALS, BATCH_SIZE):
        batch = []
        for j in range(i, min(i + BATCH_SIZE, TOTAL_INTERVALS)):
            # Calculate the timestamp for this interval.
            timestamp = START_DATE + datetime.timedelta(seconds=20 * j)
            # Generate a utilization value using Gaussian noise around the baseline.
            utilization = random.gauss(baseline, 10)
            utilization = max(0, min(utilization, 100))
            
            # Determine temperature based on utilization.
            if utilization < 40:
                temperature = random.uniform(30, 50)
            elif utilization < 70:
                temperature = random.uniform(50, 70)
            else:
                temperature = random.uniform(70, 95)
            
            # Calculate memory used roughly proportional to utilization (with noise).
            memory_used = (utilization / 100) * mem_total * random.uniform(0.9, 1.1)
            
            # Determine power consumption based on utilization.
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
        try:
            db.insert_gpu_metrics_batch(batch)
        except Exception as e:
            print(f"Error inserting batch for GPU {gpu_id}: {e}")
        inserted = i + len(batch)
        print(f"GPU {gpu_id}: inserted {inserted} out of {TOTAL_INTERVALS} intervals.", flush=True)
    db.close()

def simulate_metrics_for_gpu_chunk(chunk):
    """
    Process a chunk of GPU records sequentially.
    Each GPU in the chunk will have its 2-day metrics simulated.
    """
    for gpu in chunk:
        simulate_metrics_for_gpu(gpu)

def chunkify(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def simulate_gpu_metrics():
    """
    Simulate GPU metrics for all GPUs for a fixed number of intervals (2 days worth) and then exit.
    """
    gpu_list = load_gpu_list()
    print(f"Simulating 2 days of data (20 sec intervals, TOTAL_INTERVALS={TOTAL_INTERVALS}) for {len(gpu_list)} GPUs.")
    
    num_workers = NUM_WORKERS
    chunk_size = len(gpu_list) // num_workers
    if len(gpu_list) % num_workers != 0:
        chunk_size += 1
        
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        chunks = list(chunkify(gpu_list, chunk_size))
        futures = [executor.submit(simulate_metrics_for_gpu_chunk, chunk) for chunk in chunks]
        for future in futures:
            future.result()
    print(f"Completed inserting metrics for {len(gpu_list)} GPUs.")

if __name__ == "__main__":
    simulate_gpu_metrics()
