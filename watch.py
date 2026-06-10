from playwright.sync_api import sync_playwright

url = "https://www.tmdn.org/tmview/#/tmview/results?page=1&pageSize=30&criteria=C&basicSearch=LG&sortColumn=applicationDate&desc=true"

def log_response(response):
    if "search/results" in response.url:
        print("FOUND:", response.url)

        try:
            print(response.text()[:5000])
        except:
            pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.on("response", log_response)

    page.goto(url)

    page.wait_for_timeout(10000)

    browser.close()
