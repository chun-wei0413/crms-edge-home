# CRMS 測試套件

這個目錄包含了基於邊緣運算居家微服務之計算資源管理系統（CRMS）的完整測試套件。

## 📁 目錄結構

```
tests/
├── unit/                    # 單元測試
│   ├── test_config.py      # 系統配置測試
│   └── __init__.py
├── integration/             # 整合測試
│   ├── test_video_upload.py # 影片上傳整合測試
│   └── __init__.py
├── e2e/                     # 端到端測試
│   ├── system_test_simple.py # 系統整體測試
│   ├── e2e_test.py         # 完整 E2E 測試
│   ├── simple_e2e_test.py  # 簡化 E2E 測試
│   ├── final_system_test.py # 最終系統測試
│   └── __init__.py
├── test_runner.py           # 統一測試執行器
├── requirements.txt         # 測試依賴套件
├── pytest.ini             # pytest 配置
├── __init__.py             # 測試套件初始化
└── README.md               # 本檔案
```

## 🚀 快速開始

### 1. 安裝測試依賴
```bash
pip install -r tests/requirements.txt
```

### 2. 確保系統運行
```bash
# 啟動所有服務
docker-compose up -d

# 確認服務狀態
docker-compose ps
```

### 3. 執行測試
```bash
# 執行所有測試
python -m tests.test_runner

# 或使用 pytest
pytest tests/
```

## 🔧 測試執行器使用方法

### 基本用法
```bash
# 執行所有測試
python -m tests.test_runner

# 執行特定類型測試
python -m tests.test_runner --type unit
python -m tests.test_runner --type integration  
python -m tests.test_runner --type e2e

# 詳細輸出模式
python -m tests.test_runner --verbose
```

### 輸出說明
- ✅ **通過**: 測試成功完成
- ❌ **失敗**: 測試失敗，需要檢查
- ℹ️  **資訊**: 一般資訊訊息

## 📝 測試類型詳細說明

### 🔬 單元測試 (Unit Tests)
位置: `tests/unit/`

測試個別組件的獨立功能：
- **test_config.py**: 驗證系統配置檔案、專案結構

```bash
# 單獨執行
python tests/unit/test_config.py
```

### 🔗 整合測試 (Integration Tests)
位置: `tests/integration/`

測試服務間的整合：
- **test_video_upload.py**: 測試影片上傳與處理流程

```bash
# 單獨執行
python tests/integration/test_video_upload.py
```

### 🌐 端到端測試 (E2E Tests)
位置: `tests/e2e/`

測試完整的使用者工作流程：
- **system_test_simple.py**: 系統基本功能測試（推薦）
- **e2e_test.py**: 完整功能測試
- **simple_e2e_test.py**: 簡化版測試
- **final_system_test.py**: 最終驗證測試

```bash
# 推薦使用的系統測試
python tests/e2e/system_test_simple.py
```

## 🔨 使用 pytest

### 基本 pytest 命令
```bash
# 執行所有測試
pytest tests/

# 執行特定目錄
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# 詳細輸出
pytest tests/ -v

# 僅顯示失敗
pytest tests/ -q
```

### 測試覆蓋率
```bash
# 產生覆蓋率報告
pytest tests/ --cov=. --cov-report=html

# 查看覆蓋率報告
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

### 標記測試
```bash
# 執行特定標記的測試
pytest tests/ -m unit
pytest tests/ -m integration
pytest tests/ -m e2e
pytest tests/ -m slow
```

## ⚙️ 測試配置

### 環境變數
測試套件使用以下預設配置（在 `tests/__init__.py` 中定義）：

```python
TEST_CONFIG = {
    "MINIO_URL": "http://localhost:9000",
    "CLEANING_SERVICE_URL": "http://localhost:5001", 
    "POSE_SERVICE_URL": "http://localhost:5000",
    "WEB_FRONTEND_URL": "http://localhost:3000",
    "TEST_VIDEO_PATH": "video/test1.mp4",
    "TEST_TIMEOUT": 30
}
```

### pytest 配置
`pytest.ini` 檔案包含了 pytest 的預設設定：
- 測試檔案模式: `test_*.py`
- 測試函數模式: `test_*`
- 標記定義: unit, integration, e2e, slow

## 🐛 故障排除

### 常見問題

**Q: 測試執行器無法找到模組**
```bash
# 確保在專案根目錄執行
cd /path/to/crms
python -m tests.test_runner
```

**Q: 服務連接失敗**
```bash
# 確認所有服務都在運行
docker-compose ps

# 檢查服務日誌
docker-compose logs
```

**Q: 測試影片不存在**
```bash
# 確認測試影片檔案存在
ls video/test1.mp4

# 如果沒有，可以使用任意 MP4 檔案
cp your-video.mp4 video/test1.mp4
```

### 除錯模式
```bash
# 使用 pytest 的除錯模式
pytest tests/ --pdb

# 在失敗時進入除錯
pytest tests/ --pdbcls=IPython.terminal.debugger:Pdb
```

## 🎯 最佳實踐

### 撰寫新測試
1. **單元測試**: 測試單一功能，快速執行
2. **整合測試**: 測試服務互動，適中複雜度
3. **E2E 測試**: 測試完整流程，較慢但全面

### 測試命名
- 檔案: `test_*.py`
- 函數: `test_*`
- 類別: `Test*`

### 斷言建議
```python
# 好的斷言 - 具體且有意義
assert response.status_code == 200, f"API 回應失敗: {response.text}"

# 避免 - 不夠具體
assert response.ok
```

## 📊 測試報告

執行測試後，你會看到類似以下的報告：

```
🚀 CRMS 測試套件執行器
==================================================
🔬 執行單元測試...
   ✅ 配置測試通過
🔗 執行整合測試...  
   ✅ 影片上傳整合測試通過
🌐 執行端到端測試...
   ✅ 系統整體測試通過

==================================================
📊 測試結果摘要:
  單元測試: ✅ 通過
  整合測試: ✅ 通過  
  端到端測試: ✅ 通過

🎉 所有測試通過!
```

## 🤝 貢獻測試

歡迎為 CRMS 專案貢獻測試用例！

1. 在適當的目錄中新增測試檔案
2. 遵循現有的測試模式和命名規範  
3. 確保測試可以獨立執行
4. 新增適當的文檔說明

---

有任何測試相關問題，請查看主要的 [README.md](../README.md) 或建立 Issue。