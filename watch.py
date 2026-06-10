import requests

print("START")

url = "https://www.google.com"

r = requests.get(url)

print("STATUS =", r.status_code)

print("END")
