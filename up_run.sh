#!/bin/bash
git pull
# 设置镜像和容器名称
IMAGE_NAME="titafox/dageio:v2"
CONTAINER_NAME="dageio_container"

# 停止并删除正在运行的容器
docker ps | grep $CONTAINER_NAME | awk '{print $1}' | xargs -I {} docker stop {}
docker ps -a | grep $CONTAINER_NAME | awk '{print $1}' | xargs -I {} docker rm {}

# 删除旧镜像
docker rmi $IMAGE_NAME

# 从GitHub拉取最新代码
git pull

# 构建新镜像
docker build -t $IMAGE_NAME . --load

# 运行新容器
docker run --network="host" -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME

# 显示正在运行的容器
docker ps
