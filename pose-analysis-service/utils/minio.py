import os

from minio import Minio
from minio.error import S3Error

class MinioClientManager:
    def __init__(self, url, access_key, secret_key, secure=True):
        self.minio_client = Minio(
            url,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
    def save_resource(self,bucket_name,file_name):
        if not self.minio_client.bucket_exists(bucket_name):
            self.minio_client.make_bucket(bucket_name)
        try:
            with open(file_name, "rb") as file_data:
                file_stat = os.stat(file_name)
                self.minio_client.put_object(
                    bucket_name,
                    file_name,
                    file_data,
                    file_stat.st_size
                )
            print("Upload successful")
        except S3Error as exc:
            print("Error occurred:", exc)
            return False
        finally:
            return True

    def get_resource(self,bucket,filename):
        return self.minio_client.get_object(bucket, filename)


