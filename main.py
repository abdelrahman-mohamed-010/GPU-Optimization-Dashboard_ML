from gpu.detector import GPUDetector
from gpu.simulation import generate_gpu_static_data, save_static_data_to_db
from monitoring.monitor import monitor_gpus

from db.database import DatabaseManager
import asyncio
import threading
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
    db_manager.create_tables()
    for gpu in gpus:
        db_manager.insert_gpu_statics(gpu)
    db_manager.close()

def start_monitoring_loop():
    asyncio.run(monitor_gpus())

def main():
    
    ##commented part is for the single local gpu
    # gpus = collect_static_data()
    # if not gpus:
    #     print("No GPUs detected on any host. Exiting.")
    #     return
    # save_static_data(gpus)

    # simulation data
    df_static = generate_gpu_static_data(num_gpus=5000)
    # df_static.to_csv("static_gpu_data.csv", index=False) For save data into the csv format
    save_static_data_to_db(df_static)

    monitor_thread = threading.Thread(target=start_monitoring_loop,daemon=True)
    monitor_thread.start()

    print("Monitoring ans scheduling are running. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.....")

if __name__ =="__main__":
    main()