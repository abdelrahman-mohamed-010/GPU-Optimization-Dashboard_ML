import subprocess
import csv
import io
from .models import GPU


class GPUDetector:
    def __init__(self):
        self.gpus=[]
    
    def run_command(self, command):
        try:
            output=subprocess.check_output(command, shell=True, text=True)
            return output
        except subprocess.CalledProcessError as e:
            print(f"Command '{command}' failed: {e}")
            return ""
    
    def detect_gpus(self):
        lspci_output = self.run_command("lspci | grep -i vga")
        if "NVIDIA" in lspci_output:
            self.detect_nvidia()
        return self.gpus
    
    def detect_nvidia(self):
        cmd="nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv,noheader"
        output=self.run_command(cmd)
        if not output:
            return
        reader=csv.reader(io.StringIO(output))
        for idx, row in enumerate(reader):
            try:
                name = row[0].strip()
                mem_str = row[1].strip()
                if "GiB" in mem_str:
                    mem_total = float(mem_str.split()[0])
                elif "MiB" in mem_str:
                    mem_total = float(mem_str.split()[0]) / 1024  
                else:
                    mem_total = float(mem_str)
                compute_tflops=float(row[2].strip())
                bandwidth=936 if "RTX 3090" in name else 0
                gpu = GPU(id=f"local-{idx}",model=name,memory_total_gb=mem_total,compute_tflops=compute_tflops, bandwidth_gbps=bandwidth)
                self.gpus.append(gpu)
            except Exception as e:
                print(f"Error parsing Nvidia GPU details {e}")
    
    def detect_amd(self):
        cmd="rocm-smi --showhw"
        output=self.run_command(cmd)
        if not output:
            return
        