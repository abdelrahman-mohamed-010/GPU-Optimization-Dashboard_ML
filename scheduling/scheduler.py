import time
import random
import threading
from queue import Queue
from db.database import DatabaseManager
from scheduling.nnp_predictor import predict_best_gpu

def predict_best_gpu(task, gpu_states):
    best_gpu = None
    best_util = 100.0
    for state in gpu_states:
        dynamic = state.get("dynamic")
        if dynamic:
            util = dynamic[2] 
            if util < best_util:
                best_util = util
                best_gpu = state["static"][0]
    return best_gpu


def scheduler_loop(scheduler_interval=30, task_queue=None):
    db = DatabaseManager()
    db.connect()
    try:
        while True:
            cursor = db.conn.cursor()
            gpu_ids = [row[0] for row in cursor.execute("SELECT id FROM gpu_static").fetchall()]
            gpu_features = {}
            for gpu_id in gpu_ids:
                state = db.get_gpu_state(gpu_id)
                if state["static"] is not None and state["dynamic"] is not None:
                    static = state["static"]
                    dynamic = state["dynamic"]
                    total_memory = static[2] 
                    utilization = dynamic[2]  
                    memory_used = dynamic[3]  
                    temperature = dynamic[4]  
                    power_w = dynamic[5]      
                    features = [
                        utilization / 100.0, 
                        memory_used / total_memory if total_memory > 0 else 0,  
                        temperature / 100.0,
                        power_w / 400.0                                  
                    ]
                    while len(features) < 10:
                        features.append(0.0)
                    gpu_features[gpu_id] = features
            if task_queue is not None:
                while not task_queue.empty():
                    task = task_queue.get()
                    best_gpu = predict_best_gpu(task, gpu_features)
                    if best_gpu is None and gpu_ids:
                        best_gpu = random.choice(gpu_ids)
                    print(f"Task {task} assigned to GPU {best_gpu} based on NNP prediction.")
            else:
                print("No task queue provided. Scheduler running without tasks.")
            
            threshold = 80
            for gpu_id, features in gpu_features.items():
                util_percent = features[0] * 100
                if util_percent > threshold:
                    print(f"GPU {gpu_id} is overloaded (utilization {util_percent}%). Triggering reassignment...")
            
            time.sleep(scheduler_interval)
    except KeyboardInterrupt:
        print("Scheduler loop interrupted.")
    finally:
        db.close()

def start_scheduler():
    task_queue = Queue()
    for i in range(1,101):
        task_queue.put(f"TASK_{i}")
        scheduler_thread = threading.Thread(target=scheduler_loop, args=(30, task_queue))
        scheduler_thread.start()
        return scheduler_thread