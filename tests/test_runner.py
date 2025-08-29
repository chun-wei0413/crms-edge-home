#!/usr/bin/env python3
"""
CRMS 測試執行器
統一執行所有測試類型的主程式
"""

import sys
import argparse
import subprocess
from pathlib import Path
from . import TEST_CONFIG

def run_unit_tests():
    """執行單元測試"""
    print("🔬 執行單元測試...")
    # 當有單元測試檔案時執行
    unit_dir = Path(__file__).parent / "unit"
    test_files = list(unit_dir.glob("test_*.py"))
    
    if not test_files:
        print("ℹ️  目前沒有單元測試檔案")
        return True
        
    for test_file in test_files:
        print(f"   執行 {test_file.name}")
        result = subprocess.run([sys.executable, str(test_file)])
        if result.returncode != 0:
            return False
    return True

def run_integration_tests():
    """執行整合測試"""
    print("🔗 執行整合測試...")
    integration_dir = Path(__file__).parent / "integration"
    
    # 執行影片上傳測試
    video_test = integration_dir / "test_video_upload.py"
    if video_test.exists():
        print("   執行影片上傳整合測試")
        result = subprocess.run([sys.executable, str(video_test)])
        if result.returncode != 0:
            return False
    
    return True

def run_e2e_tests():
    """執行端到端測試"""
    print("🌐 執行端到端測試...")
    e2e_dir = Path(__file__).parent / "e2e"
    
    # 執行系統測試
    system_test = e2e_dir / "system_test_simple.py"
    if system_test.exists():
        print("   執行系統整體測試")
        result = subprocess.run([sys.executable, str(system_test)])
        if result.returncode != 0:
            return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="CRMS 測試執行器")
    parser.add_argument("--type", choices=["unit", "integration", "e2e", "all"], 
                       default="all", help="測試類型")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="詳細輸出")
    
    args = parser.parse_args()
    
    print("🚀 CRMS 測試套件執行器")
    print("=" * 50)
    
    if args.verbose:
        print("測試配置:")
        for key, value in TEST_CONFIG.items():
            print(f"  {key}: {value}")
        print()
    
    results = []
    
    if args.type in ["unit", "all"]:
        results.append(("單元測試", run_unit_tests()))
    
    if args.type in ["integration", "all"]:
        results.append(("整合測試", run_integration_tests()))
    
    if args.type in ["e2e", "all"]:
        results.append(("端到端測試", run_e2e_tests()))
    
    print("\n" + "=" * 50)
    print("📊 測試結果摘要:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ 通過" if passed else "❌ 失敗"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有測試通過!")
        sys.exit(0)
    else:
        print("\n⚠️  部分測試失敗!")
        sys.exit(1)

if __name__ == "__main__":
    main()