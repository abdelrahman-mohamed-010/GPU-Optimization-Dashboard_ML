import argparse
import time

def simulate_cluster(cluster_id, gpus):
    print(f"Simulating cluster {cluster_id} with {gpus} GPUs.")
    try:
        while True:
            print(f"Cluster {cluster_id}: Simulation active...")
            time.sleep(3)
    except KeyboardInterrupt:
        print(f"Cluster {cluster_id} simulation interrupted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a GPU cluster")
    parser.add_argument("--cluster_id", type=int, required=True, help="Cluster ID")
    parser.add_argument("--gpus", type=int, required=True, help="Number of GPUs in the cluster")
    args = parser.parse_args()
    
    simulate_cluster(args.cluster_id, args.gpus)
