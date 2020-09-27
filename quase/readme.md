Build for: https://github.com/CogComp/QuASE

Build:

```
docker build -t woffee/quase:v1 .
```


Test:
```
docker run -v /Users/woffee/www/docker/quase:/home -w /home -it woffee/quase:v1 python test.py

# -v 把主机的目录挂载到容器的 /home 目录
# -w 把容器的 /home 目录设置为工作目录
```