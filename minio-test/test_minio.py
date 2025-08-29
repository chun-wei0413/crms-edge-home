#!/usr/bin/env python3
"""
MinIO 連線測試程式
"""
import os
from minio import Minio
from minio.error import S3Error
import requests
import time

def test_minio_connection():
    """測試 MinIO 連線"""
    try:
        # MinIO 連線設定
        client = Minio(
            "localhost:9000",
            access_key="DefaultUser",
            secret_key="DefaultPassword",
            secure=False
        )
        
        # 測試連線
        print("正在測試 MinIO 連線...")
        buckets = client.list_buckets()
        print(f"連線成功！找到 {len(buckets)} 個儲存桶:")
        for bucket in buckets:
            print(f"  - {bucket.name} (建立時間: {bucket.creation_date})")
            
        # 建立測試儲存桶
        bucket_name = "test-bucket"
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"建立儲存桶: {bucket_name}")
        else:
            print(f"儲存桶已存在: {bucket_name}")
            
        print("MinIO 連線測試完成！")
        return True
        
    except S3Error as e:
        print(f"MinIO 連線失敗: {e}")
        return False
    except Exception as e:
        print(f"未知錯誤: {e}")
        return False

def wait_for_minio():
    """等待 MinIO 服務啟動"""
    print("等待 MinIO 服務啟動...")
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:9000/minio/health/live", timeout=5)
            if response.status_code == 200:
                print("MinIO 服務已啟動!")
                return True
        except:
            pass
        
        print(f"嘗試 {i+1}/{max_attempts}...")
        time.sleep(2)
    
    print("MinIO 服務啟動超時")
    return False

if __name__ == "__main__":
    if wait_for_minio():
        test_minio_connection()
    else:
        print("無法連線到 MinIO 服務")