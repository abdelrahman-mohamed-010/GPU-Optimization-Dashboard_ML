import os
import random
from datetime import datetime, timedelta
import pandas as pd
import docker
import time

gpu_specs = {
    "RTX 4090": {"memory_total_gb": 24, "compute_tflops": 82, "bandwidth_gbps": 1008},
    "RTX 4080": {"memory_total_gb": 16, "compute_tflops": 49, "bandwidth_gbps": 720},
    "RTX 7900": {"memory_total_gb": 20, "compute_tflops": 60, "bandwidth_gbps": 600},
    "A100 80GB": {"memory_total_gb": 80, "compute_tflops": 19.5, "bandwidth_gbps": 1555},
    "V100 32GB": {"memory_total_gb": 32, "compute_tflops": 15, "bandwidth_gbps": 900},
    "V100 16GB": {"memory_total_gb": 16, "compute_tflops": 15, "bandwidth_gbps": 900},
    "H100": {"memory_total_gb": 80, "compute_tflops": 60, "bandwidth_gbps": 2000}
}

gpu_models = list(gpu_specs.keys())

def generate_gpu_static_data(num_gpus=5000):
    static_data = []
    for i in range(1, num_gpus + 1):
        gpu_id = f"GPU_{i}"
        model = random.choice(gpu_models)
        specs = gpu_specs[model]
        static_data.append({
            "id": gpu_id,
            "model": model,
            "memory_total_gb": specs["memory_total_gb"],
            "compute_tflops": specs["compute_tflops"],
            "bandwidth_gbps": specs["bandwidth_gbps"]
        })
        if i % 10000 == 0:
            print(f"Generated static data for {i} GPUs...")
    df_static = pd.DataFrame(static_data)
    return df_static

def generate_gpu_dynamic_metrics(static_df, num_timesteps=10, interval_seconds=60):
    dynamic_data = []
    start_time = datetime.now()

    for idx, row in static_df.iterrows():
        memory_total = row["memory_total_gb"]
        for t in range(num_timesteps):
            timestamp = start_time + timedelta(seconds=t * interval_seconds)
            utilization = round(random.uniform(0, 100), 2)

            if utilization < 20:
                mem_used = random.uniform(0.05 * memory_total, 0.3 * memory_total)
            elif utilization < 60:
                mem_used = random.uniform(0.3 * memory_total, 0.7 * memory_total)
            else:
                mem_used = random.uniform(0.7 * memory_total, memory_total)
            mem_used = round(min(mem_used, memory_total), 2)

            if utilization < 20:
                temperature = round(random.uniform(30, 50), 2)
            elif utilization < 60:
                temperature = round(random.uniform(50, 70), 2)
            else:
                temperature = round(random.uniform(70, 90), 2)

            if utilization < 20:
                power = round(random.uniform(50, 150), 2)
            elif utilization < 60:
                power = round(random.uniform(150, 250), 2)
            else:
                power = round(random.uniform(240, 400), 2)

            dynamic_data.append({
                "id": row["id"],
                "timestamp": timestamp,
                "utilization": utilization,
                "memory_used_gb": mem_used,
                "temperature": temperature,
                "power_w": power
            })
        if (idx + 1) % 10000 == 0:
            print(f"Generated dynamic metrics for {idx + 1} GPUs...")
    df_dynamic = pd.DataFrame(dynamic_data)
    return df_dynamic

def generate_task_gpu_pairs(num_tasks=1000000, static_df=None):
    if static_df is None:
        raise ValueError("Static Data must be provided.")
    
    gpu_ids = static_df["id"].tolist()
    gpu_memory_lookup = static_df.set_index("id")["memory_total_gb"].to_dict()

    task_data = []
    for task_id in range(1, num_tasks + 1):
        gpu_id = random.choice(gpu_ids)
        total_memory = gpu_memory_lookup[gpu_id]
        utilization = round(random.uniform(0, 100), 2)
        if utilization < 20:
            mem_used = random.uniform(0.05 * total_memory, 0.3 * total_memory)
        elif utilization < 60:
            mem_used = random.uniform(0.3 * total_memory, 0.7 * total_memory)
        else:
            mem_used = random.uniform(0.7 * total_memory, total_memory)
        mem_used = round(min(mem_used, total_memory), 2)
        task_data.append({
            "task_id": f"TASK_{task_id}",
            "gpu_id": gpu_id,
            "utilization": utilization,
            "memory_total_gb": mem_used
        })
        if task_id % 100000 == 0:
            print(f"Generated {task_id} task-GPU pairs...")
    df_tasks = pd.DataFrame(task_data)
    return df_tasks

def simulate_clusters(num_clusters=50, gpus_per_cluster=1000):
    client = docker.from_env()
    containers = []
    image_name = "gpu_simulation:latest"

    for cluster_id in range(1, num_clusters + 1):
        container_name = f"cluster_{cluster_id}"
        print(f"Starting simulation for Cluster {cluster_id} with {gpus_per_cluster} GPUs.")
        
        try:
            existing_container = client.containers.get(container_name)
            print(f"Container {container_name} already exists. Removing it...")
            existing_container.remove(force=True)
        except docker.errors.NotFound:
            pass
        except Exception as e:
            print(f"Error checking container {container_name}: {e}")
        
        try:
            container = client.containers.run(
                image_name,
                command=["--cluster_id", str(cluster_id), "--gpus", str(gpus_per_cluster)],
                detach=True,
                name=container_name,
                remove=True
            )
            containers.append(container)
        except Exception as e:
            print(f"Error starting container for Cluster {cluster_id}: {e}")
        
        time.sleep(0.5)
    return containers
