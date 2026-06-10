from playwright.sync_api import sync_playwright

url = "https://www.tmdn.org/tmview/#/tmview/results?page=1&pageSize=30&criteria=C&basicSearch=LG&sortColumn=applicationDate&desc=true"

print("START")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(url)

    page.wait_for_timeout(5000)

    print("TITLE:", page.title())

    browser.close()

print("END")
