import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===== 環境變數 =====
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_TO = os.environ["EMAIL_TO"]

# ===== 讀取內容 =====
with open("thoughts.txt", "r", encoding="utf-8") as f:
    body = f.read()

# ===== 讀取每日題目 =====
with open("daily.json", encoding="utf-8") as f:
    daily = json.load(f)

# ===== Email 組裝 =====
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg["Subject"] = f"📘 LeetCode Daily Coach {daily['question']['questionFrontendId']}. {daily['question']['title']}"

msg.attach(MIMEText(body, "plain", "utf-8"))

# ===== SMTP (Gmail) =====
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL_USER, EMAIL_PASS)
server.send_message(msg)
server.quit()

print("✅ Email sent successfully")
