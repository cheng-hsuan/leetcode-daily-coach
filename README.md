# leetcode-daily-coach

一個簡單的自動化流水線：抓取 LeetCode 每日題目，使用 Google Gemini（GenAI）生成教學思路，並透過 Email 寄送給指定收件者。

## 檔案摘要
- [requirements.txt](requirements.txt)：專案相依套件（requests、google-genai）。
- [scripts/fetch_daily.py](scripts/fetch_daily.py)：向 LeetCode GraphQL 取得今日題目，輸出 `daily.json`。
- [scripts/generate_thoughts.py](scripts/generate_thoughts.py)：讀取 `daily.json`，呼叫 Google Gemini 生成教學內容，輸出 `thoughts.txt`（需 `GOOGLE_API_KEY`）。
- [scripts/send_email.py](scripts/send_email.py)：讀取 `thoughts.txt` 與 `daily.json`，透過 Gmail SMTP 寄出（需 `EMAIL_USER`、`EMAIL_PASS`、`EMAIL_TO`）。

## 前置條件
- Python 3.9+（建議 3.10+）
- Google GenAI（Gemini）可用的 API Key
- Gmail 帳號（若使用 Gmail SMTP，建議以 App Password）

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
請在執行前設定下列環境變數（範例為 PowerShell）：
```powershell
$env:GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
$env:EMAIL_USER = 'you@example.com'
$env:EMAIL_PASS = 'your_smtp_password_or_app_password'
$env:EMAIL_TO   = 'recipient@example.com'
```

(在 macOS / Linux 可用 `export` 指令設定環境變數。)

## 使用流程（請從專案根目錄執行）
1. 抓取今日題目（產生 `daily.json`）：
```powershell
python .\scripts\fetch_daily.py
```

2. 生成教學思路（需 `GOOGLE_API_KEY`，產生 `thoughts.txt`）：
```powershell
python .\scripts\generate_thoughts.py
```

3. 寄出 Email（需 `EMAIL_USER`、`EMAIL_PASS`、`EMAIL_TO`）：
```powershell
python .\scripts\send_email.py
```

成功時，`send_email.py` 會在 console 顯示 `✅ Email sent successfully`。

## 輸出檔案
- `daily.json`：LeetCode 回傳的每日題目 JSON（包含 `questionFrontendId`、`title`、`difficulty`、`content` 等）。
- `thoughts.txt`：由 Gemini 生成的教學內容（純文字）。
