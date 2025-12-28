import os
import requests
from flask import Flask, render_template, request, jsonify, session
from google import genai

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Gemini 模型（與 generate_thoughts.py 相同）
MODEL = "gemini-2.5-flash-lite"

# 初始化 Gemini 客戶端
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# 語言專家 system prompt
SYSTEM_PROMPTS = {
    "Java": "You are an expert Java programmer. When providing examples, always use Java. Help the user understand Java syntax, concepts, and best practices. Respond in Traditional Chinese, but keep code and technical terms in English.",
    "Kotlin": "You are an expert Kotlin programmer. When providing examples, always use Kotlin. Help the user understand Kotlin syntax, concepts, and best practices. Respond in Traditional Chinese, but keep code and technical terms in English.",
    "Python3": "You are an expert Python programmer. When providing examples, always use Python 3. Help the user understand Python syntax, concepts, and best practices. Respond in Traditional Chinese, but keep code and technical terms in English.",
}

# LeetCode GraphQL Queries
DAILY_QUERY = """
query questionOfToday {
  activeDailyCodingChallengeQuestion {
    date
    link
    question {
      questionFrontendId
      title
      titleSlug
      difficulty
      content
    }
  }
}
"""

QUESTION_BY_SLUG_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    difficulty
    content
  }
}
"""

QUESTION_LIST_QUERY = """
query problemsetQuestionList($filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: ""
    limit: 1
    skip: 0
    filters: $filters
  ) {
    questions: data {
      titleSlug
    }
  }
}
"""


def fetch_daily_question():
    """獲取當日 LeetCode 題目"""
    res = requests.post(
        "https://leetcode.com/graphql",
        json={"query": DAILY_QUERY},
        headers={"Content-Type": "application/json"},
    )
    data = res.json()["data"]["activeDailyCodingChallengeQuestion"]
    return {
        "questionFrontendId": data["question"]["questionFrontendId"],
        "title": data["question"]["title"],
        "titleSlug": data["question"]["titleSlug"],
        "difficulty": data["question"]["difficulty"],
        "content": data["question"]["content"],
        "link": f"https://leetcode.com{data['link']}",
    }


def fetch_question_by_id(frontend_id):
    """根據 questionFrontendId 獲取題目"""
    # 先用 frontendQuestionId filter 找到 titleSlug
    res = requests.post(
        "https://leetcode.com/graphql",
        json={
            "query": QUESTION_LIST_QUERY,
            "variables": {"filters": {"searchKeywords": str(frontend_id)}},
        },
        headers={"Content-Type": "application/json"},
    )
    data = res.json()
    questions = data.get("data", {}).get("problemsetQuestionList", {}).get("questions", [])

    if not questions:
        return None

    title_slug = questions[0]["titleSlug"]

    # 用 titleSlug 獲取完整題目資訊
    res = requests.post(
        "https://leetcode.com/graphql",
        json={"query": QUESTION_BY_SLUG_QUERY, "variables": {"titleSlug": title_slug}},
        headers={"Content-Type": "application/json"},
    )
    question = res.json()["data"]["question"]

    return {
        "questionFrontendId": question["questionFrontendId"],
        "title": question["title"],
        "titleSlug": question["titleSlug"],
        "difficulty": question["difficulty"],
        "content": question["content"],
        "link": f"https://leetcode.com/problems/{question['titleSlug']}/",
    }


def generate_solution(question, language):
    """根據題目和語言產生可提交的解法"""
    prompt = f"""You are an expert {language} programmer.

LeetCode Problem:
Title: {question['title']}
Difficulty: {question['difficulty']}

Problem description:
{question['content']}

請用 {language} 提供一個可以直接在 LeetCode 提交的完整解法。

要求：
1. 使用繁體中文說明解題思路
2. 提供完整可執行的程式碼（可直接複製貼上到 LeetCode 提交）
3. 說明時間和空間複雜度
4. 程式碼請放在 markdown code block 中，標註語言

格式：
1. 解題思路（簡短說明）
2. 完整程式碼
3. 複雜度分析
"""

    resp = client.models.generate_content(model=MODEL, contents=prompt)
    return resp.text


@app.route("/")
def index():
    # 清空對話歷史
    session["history"] = []
    session["language"] = "Python3"
    session["question"] = None
    return render_template("index.html")


@app.route("/api/daily")
def get_daily():
    """獲取當日題目"""
    try:
        question = fetch_daily_question()
        return jsonify({"success": True, "question": question})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/question/<frontend_id>")
def get_question(frontend_id):
    """根據 ID 獲取題目"""
    try:
        question = fetch_question_by_id(frontend_id)
        if question:
            return jsonify({"success": True, "question": question})
        else:
            return jsonify({"success": False, "error": "題目不存在"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/solution", methods=["POST"])
def get_solution():
    """產生題目解法"""
    data = request.json
    question = data.get("question")
    language = data.get("language", "Python3")

    if not question:
        return jsonify({"success": False, "error": "缺少題目資訊"}), 400

    try:
        solution = generate_solution(question, language)

        # 儲存到 session
        session["question"] = question
        session["history"] = [{"role": "assistant", "content": solution}]
        session.modified = True

        return jsonify({"success": True, "solution": solution})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    language = data.get("language", "Python3")

    # 更新語言設定
    session["language"] = language

    # 取得或初始化對話歷史
    if "history" not in session:
        session["history"] = []

    # 加入用戶訊息到歷史
    session["history"].append({"role": "user", "content": user_message})

    # 建構完整 prompt（包含 system prompt 和對話歷史）
    system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["Python3"])

    # 如果有題目，加入題目資訊
    question_context = ""
    if session.get("question"):
        q = session["question"]
        question_context = f"""
Current LeetCode Problem:
Title: {q['title']} (#{q['questionFrontendId']})
Difficulty: {q['difficulty']}
Link: {q['link']}

"""

    # 組合對話歷史成完整 prompt
    conversation = f"System: {system_prompt}\n\n{question_context}"
    for msg in session["history"]:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n\n"
    conversation += "Assistant:"

    # 呼叫 Gemini API
    try:
        resp = client.models.generate_content(model=MODEL, contents=conversation)
        assistant_message = resp.text

        # 加入助手回應到歷史
        session["history"].append({"role": "assistant", "content": assistant_message})
        session.modified = True

        return jsonify({"success": True, "message": assistant_message})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/clear", methods=["POST"])
def clear():
    session["history"] = []
    session["question"] = None
    return jsonify({"success": True})


if __name__ == "__main__":
    print("🚀 Starting Code Coach at http://localhost:5000")
    app.run(debug=True, port=5000)
