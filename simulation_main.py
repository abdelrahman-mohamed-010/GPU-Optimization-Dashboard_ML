import os
import time
from gpu.simulation import (
    generate_gpu_static_data,
    generate_gpu_dynamic_metrics,
    generate_task_gpu_pairs,
    simulate_clusters
)
from config import SIMULATION_OUTPUT_DIR

def main():
    os.makedirs(SIMULATION_OUTPUT_DIR, exist_ok=True)

    print("Generating GPU static data...")
    df_static = generate_gpu_static_data(num_gpus=50000)
    static_file = os.path.join(SIMULATION_OUTPUT_DIR, "gpu_statics.csv")
    df_static.to_csv(static_file, index=False)
    print(f"GPU static data saved to {static_file}")

    print("Generating GPU dynamic metrics data...")
    df_dynamic = generate_gpu_dynamic_metrics(df_static, num_timesteps=10, interval_seconds=60)
    dynamic_file = os.path.join(SIMULATION_OUTPUT_DIR, "gpu_dynamic_metrics.csv")
    df_dynamic.to_csv(dynamic_file, index=False)
    print(f"GPU dynamic metrics data saved to {dynamic_file}")

    print("Generating task-GPU pairs for NNP training...")
    df_tasks = generate_task_gpu_pairs(num_tasks=1000000, static_df=df_static)
    task_file = os.path.join(SIMULATION_OUTPUT_DIR, "task_gpu_pairs.csv")
    df_tasks.to_csv(task_file, index=False)
    print(f"Task-GPU pairs data saved to {task_file}")

    print("Launching simulation containers for 50 GPU clusters...")
    containers = simulate_clusters(num_clusters=50, gpus_per_cluster=1000)
    print("The following simulation containers have been started:")
    for container in containers:
        print(f" - {container.name}")

    time.sleep(10)
    print("Stopping simulation containers...")
    for container in containers:
        try:
            container.reload()
            if container.status == 'running':
                container.stop()
                print(f"Container {container.name} stopped.")
            else:
                print(f"Container {container.name} is not running (status: {container.status}).")
        except Exception as e:
            print(f"Error stopping container {container.name}: {e}")

if __name__ == "__main__":
    main()
