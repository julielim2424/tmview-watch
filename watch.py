from playwright.sync_api import sync_playwright

url = "https://www.tmdn.org/tmview/#/tmview/results?page=1&pageSize=30&criteria=C&basicSearch=LG&sortColumn=applicationDate&desc=true"

def handle_request(request):
    if "search/results" in request.url:
        print("========== REQUEST ==========")

        try:
            print(request.post_data)
        except:
            pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.on("request", handle_request)

    page.goto(url)

    page.wait_for_timeout(10000)

    browser.close()
