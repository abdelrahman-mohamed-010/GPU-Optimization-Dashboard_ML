import threading
import time
from gpu.simulation import generate_static_data
from monitoring.simulate_metrics import simulate_gpu_metrics

def main():
    print("Generating static data (clusters, racks, and GPUs)...")
    generate_static_data()   # This inserts all static data into the database.
    
    # Start the dynamic GPU metrics simulation in a daemon thread.
    metrics_thread = threading.Thread(target=simulate_gpu_metrics, daemon=True)
    metrics_thread.start()
    
    print("GPU metrics simulation is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    main()
