from gpu.detector import GPUDetector
from db.database import DatabaseManager


def main():
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


    ### insert GPUs records into the sqlite3 database
    db_manager=DatabaseManager()
    db_manager.connect()
    db_manager.create_table()
    for gpu in all_gpus:
        db_manager.insert_gpu(gpu)
    db_manager.close()

if __name__ =="__main__":
    main()