# 使用官方的 Python 镜像作为基础镜像
FROM python:3.10-slim


# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件并安装依賴
# 复制项目中的所有文件到工作目录
COPY . .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 創建上傳和結果目錄
RUN mkdir -p uploads results
# 暴露端口 5000
EXPOSE 5000

# 运行应用程序
CMD ["python", "app.py"]
