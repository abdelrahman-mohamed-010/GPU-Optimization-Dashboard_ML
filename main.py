import threading
import time
from gpu.simulation import generate_static_data
from monitoring.simulate_metrics import simulate_gpu_metrics
from rl.federated_ppo import simulate_federated_training
import time

def run_rl_training():
    simulate_federated_training()

def main():
    print("Generating static data (clusters, racks, and GPUs)...")
    generate_static_data()
    
    # Start the dynamic GPU metrics simulation in a daemon thread.
    metrics_thread = threading.Thread(target=simulate_gpu_metrics, daemon=True)
    metrics_thread.start()

    # time.sleep(40)
    # rl_thread = threading.Thread(target=run_rl_training, daemon=True)
    # rl_thread.start()
    
    print("GPU metrics simulation is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    main()
