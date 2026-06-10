import requests

url = "https://www.tmdn.org/tmview/#/tmview/results?page=1&pageSize=30&criteria=C&basicSearch=LG&sortColumn=applicationDate&desc=true"

r = requests.get(url)

print("status:", r.status_code)
print(r.text[:1000])
