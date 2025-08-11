# gpu_check.py
import torch, subprocess, re

print("==== PyTorch & GPU Info ====")
print(f"PyTorch version: {torch.__version__}")
print(f"Is CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    torch_cuda = torch.version.cuda
    print(f"CUDA version (PyTorch built with): {torch_cuda}")
    print(f"cuDNN version: {torch.backends.cudnn.version()}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"--- GPU {i} ---")
        print(f"Name: {torch.cuda.get_device_name(i)}")
        print(f"Capability: {torch.cuda.get_device_capability(i)}")

    # 从 nvidia-smi 解析驱动可支持的最高 CUDA 版本
    try:
        out = subprocess.check_output(["nvidia-smi"], encoding="utf-8")
        m = re.search(r"CUDA Version:\s+(\d+\.\d+)", out)
        if m:
            drv_cuda = m.group(1)
            print(f"Max CUDA version supported by driver: {drv_cuda}")
            try:
                if float(torch_cuda) > float(drv_cuda):
                    print("⚠️ WARNING: PyTorch CUDA > driver-supported CUDA. Consider upgrading the driver.")
                else:
                    print("✅ PyTorch CUDA version is compatible with the driver.")
            except Exception:
                print("Note: could not numerically compare CUDA versions.")
        else:
            print("Could not parse CUDA version from nvidia-smi.")
    except FileNotFoundError:
        print("nvidia-smi not found. Cannot check driver CUDA compatibility.")

    print(f"Memory Allocated (MB): {torch.cuda.memory_allocated()/1024**2:.2f}")
    print(f"Memory Reserved (MB): {torch.cuda.memory_reserved()/1024**2:.2f}")
else:
    print("No GPU detected or CUDA is not available.")
