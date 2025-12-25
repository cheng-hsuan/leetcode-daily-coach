import requests
import json

QUERY = """
query questionOfToday {
  activeDailyCodingChallengeQuestion {
    date
    link
    question {
      title
      titleSlug
      difficulty
      content
    }
  }
}
"""

res = requests.post(
    "https://leetcode.com/graphql",
    json={"query": QUERY},
    headers={"Content-Type": "application/json"}
)

data = res.json()["data"]["activeDailyCodingChallengeQuestion"]

with open("daily.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
