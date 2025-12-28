import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===== 環境變數 =====
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
# 支援逗號分隔的多收件者格式，例如: "user1@gmail.com,user2@gmail.com"
EMAIL_TO_LIST = [email.strip() for email in os.environ["EMAIL_TO"].split(",")]

# ===== 讀取內容 =====
with open("thoughts.txt", "r", encoding="utf-8") as f:
    body = f.read()

# ===== 讀取每日題目 =====
with open("daily.json", encoding="utf-8") as f:
    daily = json.load(f)

# 在郵件內容最前面加入題目連結
link = daily['link']
url = f"https://leetcode.com{link}"
body = f"Link: {url}\n\n" + body

# ===== SMTP (Gmail) =====
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL_USER, EMAIL_PASS)

# ===== 對每位收件者發送郵件 =====
for recipient in EMAIL_TO_LIST:
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = f"📘 LeetCode Daily Coach {daily['question']['questionFrontendId']}. {daily['question']['title']}"
    msg.attach(MIMEText(body, "plain", "utf-8"))
    server.send_message(msg)
    print(f"✅ Email sent to {recipient}")

server.quit()

print(f"✅ All emails sent successfully ({len(EMAIL_TO_LIST)} recipients)")
