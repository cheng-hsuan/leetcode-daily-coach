import os
import json
from google import genai

# Gemini 模型
MODEL = "gemini-2.5-flash-lite"

# 讀取題目
with open("daily.json", encoding="utf-8") as f:
    daily = json.load(f)

prompt = f"""
You are a senior algorithm coach.

LeetCode Daily Problem:
Title: {daily['question']['title']}
Difficulty: {daily['question']['difficulty']}
Link: https://leetcode.com{daily['link']}

Problem description (English):
{daily['question']['content']}

語言規則：
- 主要敘述請使用繁體中文
- 演算法專有名詞請保留英文（例如：Two Pointers, Sliding Window, BFS, DFS, Dynamic Programming）
- Big-O 表示法請保留英文（例如：O(n), O(n log n)）
- 程式變數名稱、函式名稱、資料結構名稱請保持原樣（例如：left, right, dp, nums, hashmap）
- 不要刻意硬翻專有名詞
- Code block 一律使用英文（但不要提供完整可執行程式碼）

Strict rules:
- DO NOT provide full executable code
- DO NOT give submission-ready solutions
- DO NOT use Markdown syntax
- DO NOT use symbols like "-", "*", "•" as bullet points
- DO NOT use code fences (```)

Formatting rules (IMPORTANT):
- 所有條列內容，請使用純文字編號格式，例如：
  (1) 第一點說明
  (2) 第二點說明
- 不要使用任何符號型 bullet
- 只能使用數字、括號、縮排來表達結構

Output structure:
1. 問題核心重述
2. 關鍵觀察
3. 解題策略選擇過程
4. Step-by-step 解題邏輯（自然語言）
5. 時間與空間複雜度
6. 常見錯誤與陷阱

每一個 section：
- 請先輸出標題（例如：2. 關鍵觀察）
- 空一行
- 再開始內容
- 若需要列點，請使用 (1)、(2)、(3) 並可用縮排表示階層
"""


# 使用 JSON 檔初始化 Gemini 客戶端
client = genai.Client(
    api_key=os.environ["GOOGLE_API_KEY"]
)

# 呼叫 Gemini API 生成內容
resp = client.models.generate_content(
    model=MODEL,
    contents=prompt
)

# 取得模型輸出
output = resp.text

# 寫成檔案
with open("thoughts.txt", "w", encoding="utf-8") as f:
    f.write(output)
