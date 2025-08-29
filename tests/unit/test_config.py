#!/usr/bin/env python3
"""
配置測試 - 測試系統配置的正確性
"""

import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_docker_compose_config():
    """測試 docker-compose.yml 配置"""
    compose_file = project_root / "docker-compose.yml"
    
    assert compose_file.exists(), "docker-compose.yml 檔案不存在"
    
    with open(compose_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查必要服務是否存在
    required_services = [
        "cleaning-robot-service",
        "pose-analysis-service", 
        "web-frontend",
        "minio"
    ]
    
    for service in required_services:
        assert service in content, f"缺少必要服務: {service}"
    
    print("✅ Docker Compose 配置測試通過")
    return True

def test_project_structure():
    """測試專案目錄結構"""
    required_dirs = [
        "cleaning-robot-service",
        "pose-analysis-service",
        "web-frontend", 
        "tests"
    ]
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        assert dir_path.exists(), f"缺少必要目錄: {dir_name}"
    
    print("✅ 專案結構測試通過")
    return True

def main():
    print("🔬 執行配置單元測試...")
    
    tests = [
        test_docker_compose_config,
        test_project_structure
    ]
    
    for test_func in tests:
        try:
            test_func()
        except AssertionError as e:
            print(f"❌ 測試失敗: {e}")
            return False
        except Exception as e:
            print(f"❌ 測試錯誤: {e}")
            return False
    
    print("🎉 所有配置測試通過!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)