from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

URL = "https://www.tmdn.org/tmview/#/tmview/results?page=1&pageSize=30&criteria=C&basicSearch=LG&sortColumn=applicationDate&desc=true"

results = []

def handle_response(response):
    global results

    if "search/results" in response.url:
        print("FOUND API:", response.url)

        try:
            data = response.json()

            trademarks = data.get("tradeMarks", [])

            for tm in trademarks:
                results.append({
                    "name": tm.get("tmName", ""),
                    "office": tm.get("tmOffice", ""),
                    "application_number": tm.get("applicationNumber", ""),
                    "application_date": tm.get("applicationDate", ""),
                    "status": tm.get("tradeMarkStatus", ""),
                    "st13": tm.get("ST13", "")
                })

        except Exception as e:
            print("ERROR:", e)

# TMView 수집
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.on("response", handle_response)

    page.goto(URL)

    page.wait_for_timeout(30000)

    browser.close()

print("FOUND", len(results), "RESULTS")

# seen.json 읽기
try:
    with open("seen.json", "r", encoding="utf-8") as f:
        seen = set(json.load(f))
except:
    seen = set()

# 신규만 추출
new_results = []

for tm in results:
    app_no = tm["application_number"]

    if app_no and app_no not in seen:
        new_results.append(tm)

print("NEW RESULTS:", len(new_results))

# 신규 없으면 종료
if len(new_results) == 0:
    print("NO NEW RESULTS")
    exit()

# 메일 본문
body = []

body.append("TMVIEW LG WATCH")
body.append("")
body.append(f"신규 건수: {len(new_results)}")
body.append("")

for tm in new_results:

    body.append(f"상표명: {tm['name']}")
    body.append(f"관청: {tm['office']}")
    body.append(f"출원번호: {tm['application_number']}")
    body.append(f"출원일: {tm['application_date']}")
    body.append(f"상태: {tm['status']}")

    if tm["st13"]:
        body.append(
            f"https://www.tmdn.org/tmview/#/tmview/detail/{tm['st13']}"
        )

    body.append("-" * 50)

email_body = "\n".join(body)

msg = MIMEMultipart()

msg["From"] = EMAIL_USER
msg["To"] = EMAIL_USER
msg["Subject"] = f"[TMVIEW] 신규 {len(new_results)}건"

msg.attach(MIMEText(email_body, "plain", "utf-8"))

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

server.login(EMAIL_USER, EMAIL_PASSWORD)

server.send_message(msg)

server.quit()

print("EMAIL SENT")

# seen.json 업데이트
for tm in new_results:
    if tm["application_number"]:
        seen.add(tm["application_number"])

with open("seen.json", "w", encoding="utf-8") as f:
    json.dump(sorted(list(seen)), f, ensure_ascii=False, indent=2)

print("SEEN UPDATED")
