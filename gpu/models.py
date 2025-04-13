
class GPU:
    def __init__(self, gpu_id, rack_id, cluster_name, model, memory_total_gb, compute_tflops, bandwidth_gbps):
        self.gpu_id = gpu_id
        self.rack_id = rack_id
        self.cluster_name = cluster_name
        self.model = model
        self.memory_total_gb = memory_total_gb
        self.compute_tflops = compute_tflops
        self.bandwidth_gbps = bandwidth_gbps

    def __repr__(self):
        return (f"GPU(gpu_id={self.gpu_id}, rack_id={self.rack_id}, cluster_name={self.cluster_name}, "
                f"model={self.model}, memory_total_gb={self.memory_total_gb}, "
                f"compute_tflops={self.compute_tflops}, bandwidth_gbps={self.bandwidth_gbps})")
