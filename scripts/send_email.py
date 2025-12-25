import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

with open("daily.json", encoding="utf-8") as f:
    daily = json.load(f)

with open("thoughts.md", encoding="utf-8") as f:
    body = f.read()

msg = MIMEMultipart()
msg["From"] = os.environ["EMAIL_USER"]
msg["To"] = os.environ["EMAIL_TO"]
msg["Subject"] = f"[LeetCode Daily] {daily['question']['difficulty']}｜{daily['question']['title']}"

msg.attach(MIMEText(body, "plain", "utf-8"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    server.send_message(msg)
