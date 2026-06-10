from playwright.sync_api import sync_playwright

url = "https://www.tmdn.org/tmview/#/tmview/results?page=1&pageSize=30&criteria=C&basicSearch=LG&sortColumn=applicationDate&desc=true"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(url)

    page.wait_for_timeout(8000)

    print("TITLE:", page.title())

    print(page.content()[:5000])

    browser.close()
