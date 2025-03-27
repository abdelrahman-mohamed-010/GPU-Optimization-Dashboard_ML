import subprocess
import pynvml
import pyopencl as cl

def detect_gpu_type(gpu_id):
    
    low_id = gpu_id.lower()
    if "nvidia" in low_id or "rtx" in low_id or "geforce" in low_id or "gtx" in low_id:
        return 'nvidia'
    elif "amd" in low_id:
        return 'amd'
    elif "intel" in low_id:
        return "intel"
    else:
        return "nvidia"
    
class GPUProfiler:
    def __init__(self, gpu_id):
        self.gpu_id = gpu_id
        self.type = detect_gpu_type(gpu_id)

    def get_dynamic(self):
        if self.type == "nvidia":
            return self._get_nvidia()
        elif self.type == "amd":
            return self._get_amd()
        else:
            return self._get_opencl()
    

    def _get_nvidia(self):
        try:
            pynvml.nvmlInit()
            index = int(self.gpu_id.split('-')[1])
            handle = pynvml.nvmlDeviceGetHandleByIndex(index)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle).used / (1024 * 1024 * 1024)
            temp = pynvml.nvmlDeviceGetTemperature(handle,0)
            power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
            return {'util':util, 'mem':mem, 'temp': temp, 'power':power}
        except Exception as e:
            print(f"Error in Nvidia dynamic collection for GPU {self.gpu_id}: {e}")
            return {'util':0, 'mem':0, 'temp': 0, 'power':0}
    
    def _get_amd(self):
        try:
            result = subprocess.run(['rocm-smi',"--showmemuse", "--showutlization"],capture_output=True,text=True)
            lines = result.stdout.splitlines()
            if len(lines)>=3:
                util = float(lines[1].split()[1])
                mem = float(lines[2].split()[1]) /1024
                return {'util':util, 'mem':mem, 'temp': 0, 'power':0}
        except Exception as e:
            print(f"Error in AMD dynamic collection for GPU {self.gpu_id}: {e}")
            return {'util':0, 'mem':0, 'temp': 0, 'power':0}
    
    def _get_opencl(self):
        try:
            platforms = cl.get_platforms()
            device = platforms[0].get_device()[0]
            mem = device.global_mem_size / 1e9
            return {'util':0, 'mem':mem, 'temp': 0, 'power':0}
        except Exception as e:
            print(f"Error in OpenCL dynamic collection for GPU {self.gpu_id}: {e}")
            return {'util':0, 'mem':0, 'temp': 0, 'power':0}