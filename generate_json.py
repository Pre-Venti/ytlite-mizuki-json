import requests
import json
from datetime import datetime

REPO = "SavageFRVR/YTLite"
OUTPUT_FILE = "ytlite.json"

api_url = f"https://api.github.com/repos/{REPO}/releases/latest"
res = requests.get(api_url)
data = res.json()

tag = data["tag_name"]
version = data["name"] or tag
ipa_url = ""
size = 0

for asset in data["assets"]:
    if asset["name"].lower().endswith(".ipa"):
        ipa_url = asset["browser_download_url"]
        size = asset["size"]
        break

if not ipa_url:
    raise Exception("Keine .ipa-Datei gefunden!")

json_data = {
    "name": "YTLite",
    "identifier": "com.savagefrvr.ytlite",
    "subtitle": "Lightweight YouTube app",
    "developer": "SavageFRVR",
    "sourceURL": "https://pre-venti.github.io/ytlite-json-source/ytlite.json",
    "iconURL": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/YouTube_social_white_squircle_%282017%29.svg/200px-YouTube_social_white_squircle_%282017%29.svg.png",
    "tintColor": "#FF0000",
    "apps": [
        {
            "name": "YTLite",
            "bundleIdentifier": "com.savagefrvr.ytlite",
            "version": version,
            "developerName": "SavageFRVR",
            "subtitle": "YouTube ohne Werbung und Tracking",
            "downloadURL": ipa_url,
            "iconURL": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/YouTube_social_white_squircle_%282017%29.svg/200px-YouTube_social_white_squircle_%282017%29.svg.png",
            "localizedDescription": "Ein modifizierter YouTube-Client mit Fokus auf Minimalismus und Datenschutz.",
            "size": size,
            "versionDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+0000"),
            "versionDescription": data.get("body", "Neues Release."),
            "tintColor": "#FF0000"
        }
    ]
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)
