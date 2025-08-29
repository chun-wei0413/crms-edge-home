# 使用官方的 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器的工作目录
COPY . /app

# 安装所需的 Python 包
RUN pip install --no-cache-dir flask

# 暴露容器的 5000 端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 运行 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
