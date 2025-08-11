## 太长不看

第一次运行，build image：

docker build -t mytorch:2.0.1-cu117 .

之后只要运行

docker compose up trainer # 默认执行 python train.py

或者 (仅启动 JupyterLab)

sudo docker compose up lab    
sudo docker compose up -d lab # 长期运行

2025/08/10

## 详细构建过程

1) gpu_check.py（复制到镜像里）
```
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
```

2) Dockerfile（把脚本打进镜像）

你的驱动上限是 CUDA 11.8；下面默认用 PyTorch 2.0.1 + CUDA 11.7 的官方镜像，稳妥。需要别的版本只改 ARG BASE_IMAGE。

```
# Dockerfile
ARG BASE_IMAGE=pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
FROM ${BASE_IMAGE}

# 可选：国内源/加速可在这里配置
WORKDIR /workspace

# 拷贝检测脚本到 PATH
COPY gpu_check.py /usr/local/bin/gpu_check.py

# 可选：预装你常用包（按需增删）
# RUN pip install -U pip && pip install jupyterlab transformers pandas matplotlib

# 默认进入 bash；需要时可直接执行 gpu_check.py 或训练脚本
CMD ["bash"]

构建：
```

docker build -t mytorch:2.0.1-cu117 .

3) 直接运行检查

docker run --gpus all --rm -it \
  -v "$PWD":/workspace -w /workspace \
  mytorch:2.0.1-cu117 \
  python /usr/local/bin/gpu_check.py

4) 训练你的 train.py

docker run --gpus all --rm -it \
  -v "$PWD":/workspace -w /workspace --ipc=host \
  mytorch:2.0.1-cu117 \
  python train.py

5) docker compose（一次配置，随时起）

docker-compose.yaml：

```
services:
  trainer:
    image: mytorch:2.0.1-cu117
    working_dir: /workspace
    command: bash -lc "python /usr/local/bin/gpu_check.py && python train.py"
    volumes:
      - ./:/workspace
      - pip_cache:/root/.cache/pip
      - hf_cache:/root/.cache/huggingface
    ipc: host
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all           # 可改为具体数量，如 1
              capabilities: [gpu]  # 必填

  lab:
    image: mytorch:2.0.1-cu117
    working_dir: /workspace
    command: bash -lc "pip install -q jupyterlab && \
                       python /usr/local/bin/gpu_check.py && \
                       jupyter lab --ip=0.0.0.0 --port=8888 --allow-root"
    ports: ["8888:8888"]
    volumes:
      - ./:/workspace
      - pip_cache:/root/.cache/pip
      - hf_cache:/root/.cache/huggingface
    ipc: host
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  pip_cache: {}
  hf_cache: {}
```

启动：

```
# 训练
docker compose up trainer

# 或仅启动 JupyterLab
docker compose up lab
```

6) 想临时用 JupyterLab？

```
docker run --gpus all -it --rm -p 8888:8888 \
  -v "$PWD":/workspace -w /workspace \
  mytorch:2.0.1-cu117 \
  bash -lc "pip install -q jupyterlab && \
            python /usr/local/bin/gpu_check.py && \
            jupyter lab --ip=0.0.0.0 --port=8888 --allow-root"
```

