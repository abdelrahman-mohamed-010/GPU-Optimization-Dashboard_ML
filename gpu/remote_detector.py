import paramiko
import csv
import io
from .models import GPU

class RemoteGPUDetector:
    def __init__(self,host, username, key_filepath,port=22):
        self.host = host
        self.username = username
        self.key_filepath = key_filepath
        self.port = port
        self.client = None
    
    def connect(self):
        self.client=paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(
                hostname=self.host,
                username=self.username,
                key_filename=self.key_filepath,
                port=self.port
            )
            print(f"Connected to remote host {self.host}")
        except Exception as e:
            print(f"Failed to connect to {self.host}: {e}")
            self.client = None
    
    def run_command(self, command):
        if not self.client:
            raise Exception("SSH client not connected.")
        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode()
        return output
    
    def detect_nvidia(self):
        gpus = []
        cmd = "nvidia-smi --query-gpu=name,memory.total, computer_Cap --format=csv,noheader"
        output =self.run_command(cmd)
        if not output:
            return gpus
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
                compute_tflops = float(row[2].strip())
                bandwidth = 936 if "RTX 3090" in name else 0

                gpu=GPU(id=f"{self.host}-{idx}",model=name,memory_total_gb=mem_total,compute_tflops=compute_tflops,bandwidth_gbps=bandwidth)
                gpus.append(gpu)
            except Exception as e:
                print(f"Error parsing Nvidia GPUs details on host {self.host}: {e}")
        return gpus
    
    def close(self):
        if self.client:
            self.client.close()
            print(f"Connection to {self.host} closed.")