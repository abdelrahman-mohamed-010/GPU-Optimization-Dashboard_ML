from gpu.detector import GPUDetector
from gpu.profiler import GPUProfiler
from db.database import DatabaseManager
import asyncio
import time

def  collect_static_data():
    all_gpus = []
    local_detector=GPUDetector()
    local_gpus=local_detector.detect_gpus()

    if local_gpus:
        print("Local GPUs detected:")
        for gpu in local_gpus:
            print(gpu)
        all_gpus.extend(local_gpus)
    else:
        print("No local GPUs detected.")
    ### AWS/Cloud GPUs logic will add here.
    return all_gpus
    
def save_static_data(gpus):
    db_manager=DatabaseManager()
    db_manager.connect()
    db_manager.create_table()
    for gpu in gpus:
        db_manager.insert_gpu(gpu)
    db_manager.close()

async def dynamic_update_loop(gpus):
    local_gpu_ids = [gpu.id for gpu in gpus if str(gpu.id).startswith("local")]
    if not local_gpu_ids:
        print("No local GPUs available for dynamic profiling.")
        return
    
    profilers = {gpu_id: GPUProfiler(gpu_id) for gpu_id in local_gpu_ids}

    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.create_dynamic_table()

    try:
        print("Starting dynamic update loop. Press Ctrl+c to strop.")
        while True:
            for gpu_id, profiler in profilers.items():
                data = profiler.get_dynamic()
                print(f"Dynamic data for GPU {gpu_id}: {data}")
                db_manager.insert_dynamic(gpu_id,data)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Dynamic update loo[ interrupted. Exiting.")
    finally:
        db_manager.close()
def main():
    
    gpus = collect_static_data()
    if not gpus:
        print("No GPUs detected on any host. Exiting.")
        return
    save_static_data(gpus)

    asyncio.run(dynamic_update_loop(gpus))

if __name__ =="__main__":
    main()