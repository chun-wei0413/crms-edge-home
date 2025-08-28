import os

def get_env_minio_host():
    return os.environ.get("MINIO_HOST","localhost:9000")
def get_env_minio_user():
    return os.environ.get("MINIO_USER","DefaultUser")
def get_env_minio_password():
    return os.environ.get("MINIO_PASSWORD","DefaultPassword")