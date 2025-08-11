# Dockerfile
ARG BASE_IMAGE=pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
FROM ${BASE_IMAGE}

# 可选：国内源/加速可在这里配置
WORKDIR /workspace

# 拷贝检测脚本到 PATH
COPY gpu_check.py /usr/local/bin/gpu_check.py

# 可选：预装你常用包（按需增删）
RUN pip install -U pip && pip install jupyterlab transformers pandas matplotlib

# 默认进入 bash；需要时可直接执行 gpu_check.py 或训练脚本
CMD ["bash"]
