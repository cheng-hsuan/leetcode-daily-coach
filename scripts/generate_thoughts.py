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

Please respond in:
- English for problem statement references
- Traditional Chinese for explanation

Strict rules:
- DO NOT provide full executable code
- DO NOT directly give submission-ready solutions

Output structure:
1. 問題核心重述
2. 關鍵觀察
3. 解題策略選擇過程
4. Step-by-step 解題邏輯（自然語言）
5. 時間與空間複雜度
6. 3 個建議自行測試的測資
7. 常見錯誤與陷阱
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
with open("thoughts.md", "w", encoding="utf-8") as f:
    f.write(output)
