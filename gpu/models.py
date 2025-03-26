
class GPU:
    def __init__(self,id, model, memory_total_gb, compute_tflops, bandwidth_gbps):
        self.id=id
        self.model=model
        self.memory_total_gb=memory_total_gb
        self.compue_tflops=compute_tflops
        self.bandwidth_gbps=bandwidth_gbps

    def __repr__(self):
        return (f"GPU(id={self.id}, model='{self.model}', memory_total_gb={self.memory_total_gb}, compue_tflops={self.compue_tflops}, bandwidth_gbps={self.bandwidth_gbps})")