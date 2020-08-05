

## Run and go into an image

	docker run -it woffee/extremenet:test /bin/bash


## CP file into docker

https://www.runoob.com/docker/docker-cp-command.html



## 列出所有的容器 ID
	docker ps -aq

## 停止所有的容器
	docker stop $(docker ps -aq)

## 删除所有的容器
	docker rm $(docker ps -aq)

## 删除所有的镜像
	docker rmi $(docker images -q)

## 复制文件
	docker cp mycontainer:/opt/file.txt /opt/local/
	docker cp /opt/local/file.txt mycontainer:/opt/


https://colobu.com/2018/05/15/Stop-and-remove-all-docker-containers-and-images/




apt-get install -y libsm6 libglib2.0-0 libxrender1 libxext6 


