
# 太长不看

使用 docker 后台运行：

    sudo docker compose up -d

想要停止的话：

    sudo docker compose down


# 我在用 docker 启动的 vscode server 中修改了文件，保存时提示我没有权限。这怎么解决？

这是典型的挂载目录权限不匹配问题：容器里运行的用户（通常是 coder，UID=1000）对你挂载进来的主机目录没有写权限，所以 VS Code（code-server）保存时报“没有权限”。

## 让容器用你主机的 UID/GID 运行

### 一次性运行：
```
docker run -it --rm -p 8080:8080 \
  -v "$(pwd)":/home/coder/project \
  --user $(id -u):$(id -g) \
  -e PASSWORD=MySecret123 \
  codercom/code-server:latest
```

### docker compose:

在同目录下创建 .env（或手动写死数值）：

```
UID=1000
GID=1000
```

docker-compose.yaml 中加：

```
services:
  code:
    image: codercom/code-server:latest
    ports: ["8080:8080"]
    volumes:
      - ./:/home/coder/project
    user: "${UID}:${GID}"
    environment:
      PASSWORD: MySecret123
```

注：在 Linux 上 echo $UID 和 id -g 看实际值；macOS/Windows 也可写成固定 1000:1000（若主机权限允许）。

