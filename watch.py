from playwright.sync_api import sync_playwright
import json

url = "https://www.tmdn.org/tmview/#/tmview/results?page=1&pageSize=30&criteria=C&basicSearch=LG&sortColumn=applicationDate&desc=true"

def handle_response(response):
    if "search/results" in response.url:
        try:
            data = response.json()

            print("RESULT COUNT:", len(data.get("tradeMarks", [])))

            for tm in data.get("tradeMarks", [])[:10]:
                print(
                    tm.get("tmName"),
                    "|",
                    tm.get("applicationNumber"),
                    "|",
                    tm.get("applicationDate")
                )

        except Exception as e:
            print("ERROR:", e)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.on("response", handle_response)

    page.goto(url)

    page.wait_for_timeout(10000)

    browser.close()
