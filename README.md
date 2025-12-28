# leetcode-daily-coach

一個 LeetCode 學習輔助工具，包含兩大功能：
1. **每日自動推送**：抓取 LeetCode 每日題目，使用 Google Gemini 生成解題思路，透過 Email 寄送給指定收件者
2. **Code Coach 網頁**：本地 AI 聊天介面，可載入任意 LeetCode 題目，自動產生可提交的解法並進行互動討論

## 檔案摘要

```
leetcode-daily-coach/
├── requirements.txt              # 專案相依套件
├── scripts/
│   ├── fetch_daily.py            # 抓取每日題目 → daily.json
│   ├── generate_thoughts.py      # AI 生成解題思路 → thoughts.txt
│   └── send_email.py             # 發送 Email（支援多收件者）
└── web/
    ├── app.py                    # Code Coach 後端（Flask + Gemini）
    └── templates/
        └── index.html            # Code Coach 前端介面
```

## 前置條件

- Python 3.9+（建議 3.10+）
- Google GenAI（Gemini）可用的 API Key
- Gmail 帳號（若使用 Gmail SMTP，建議使用 App Password）

## 安裝套件

建議使用虛擬環境後安裝：

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## 環境變數

請在執行前設定下列環境變數：

```bash
# macOS / Linux
export GOOGLE_API_KEY='YOUR_GOOGLE_API_KEY'
export EMAIL_USER='you@example.com'
export EMAIL_PASS='your_smtp_password_or_app_password'
export EMAIL_TO='recipient1@example.com,recipient2@example.com'  # 支援多收件者，以逗號分隔
```

```powershell
# Windows (PowerShell)
$env:GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
$env:EMAIL_USER = 'you@example.com'
$env:EMAIL_PASS = 'your_smtp_password_or_app_password'
$env:EMAIL_TO = 'recipient1@example.com,recipient2@example.com'
```

---

## 功能一：每日解題思路推送

自動抓取 LeetCode 每日題目，生成教學思路並 Email 寄送。

### 使用流程（從專案根目錄執行）

1. **抓取今日題目**（產生 `daily.json`）：
```bash
python scripts/fetch_daily.py
```

2. **生成解題思路**（產生 `thoughts.txt`）：
```bash
python scripts/generate_thoughts.py
```

3. **寄出 Email**：
```bash
python scripts/send_email.py
```

成功時會顯示 `✅ Email sent to xxx@example.com` 以及發送總數。

### 多收件者支援

`EMAIL_TO` 環境變數支援逗號分隔的多個 Email：
```bash
export EMAIL_TO="user1@gmail.com,user2@gmail.com,user3@gmail.com"
```

### 輸出檔案

- `daily.json`：LeetCode 每日題目資訊（題號、標題、難度、內容等）
- `thoughts.txt`：Gemini 生成的解題思路（純文字）

---

## 功能二：Code Coach 網頁

本地 AI 聊天網頁，可載入任意 LeetCode 題目，自動產生完整可提交的解法。

### 啟動方式

```bash
# 確保已設定 GOOGLE_API_KEY 環境變數
python web/app.py
```

啟動後會自動開啟瀏覽器到 http://localhost:5000

### 功能特色

- **題目載入**：輸入題目編號（如 `1`、`121`、`200`）或留空載入當日每日題目
- **題目顯示**：上方區域顯示題目原文，包含難度標籤和 LeetCode 連結
- **自動產生解法**：載入題目後，AI 會根據選擇的語言產生完整可提交的程式碼
- **語言切換**：支援 Java / Kotlin / Python3
- **互動討論**：產生解法後可繼續對話，詢問其他解法或概念
- **複製功能**：程式碼區塊右上角有複製按鈕，方便直接貼到 LeetCode 提交
- **Session 記憶**：對話歷史在當次 session 中保留，可隨時重置
