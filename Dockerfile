# 使用官方的 Python 镜像
FROM python:3.9-slim

# 在容器中设置工作目录
WORKDIR /app

# 将 requirements 文件复制到容器中
COPY requirements.txt .

# 安装所有依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 将其余的应用程序代码复制到容器中
COPY . .

# 暴露应用程序运行的端口
EXPOSE 8000

# 定义容器启动时运行应用程序的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
