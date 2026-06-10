import requests

url = "https://www.tmdn.org/tmview/api/search/results?translate=true"

payload = {
    "page": "1",
    "pageSize": "30",
    "criteria": "C",
    "basicSearch": "LG",
    "sortColumn": "applicationDate",
    "desc": "true",
    "newPage": True,
    "fields": [
        "ST13",
        "tmName",
        "tmOffice",
        "applicationNumber",
        "applicationDate",
        "tradeMarkStatus"
    ]
}

response = requests.post(url, json=payload)

print("STATUS:", response.status_code)

data = response.json()

print("TOTAL:", len(data.get("tradeMarks", [])))

for tm in data.get("tradeMarks", [])[:10]:
    print(
        tm.get("tmName"),
        "|",
        tm.get("tmOffice"),
        "|",
        tm.get("applicationNumber")
    )
