import requests

url = "https://osapi.opensports.ca/events?aliasID=big-city-volleyball"
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("✅ Status Code:", response.status_code)
print("🔍 Preview JSON:", response.text[:500])