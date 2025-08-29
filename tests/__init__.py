"""
CRMS 測試套件
基於邊緣運算居家微服務之計算資源管理系統的測試套件

包含:
- unit: 單元測試
- integration: 整合測試  
- e2e: 端到端測試
"""

__version__ = "1.0.0"
__author__ = "CRMS Team"

# 測試配置
TEST_CONFIG = {
    "MINIO_URL": "http://localhost:9000",
    "CLEANING_SERVICE_URL": "http://localhost:5001", 
    "POSE_SERVICE_URL": "http://localhost:5000",
    "WEB_FRONTEND_URL": "http://localhost:3000",
    "TEST_VIDEO_PATH": "video/test1.mp4",
    "TEST_TIMEOUT": 30
}