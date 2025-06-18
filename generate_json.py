import os
import sys
import requests
import json
from datetime import datetime

# Repo und Ausgabe
REPO = "SavageFRVR/YTLite"
OUTPUT_FILE = "ytlite.json"

# Token aus Secret
token = os.getenv("GH_TOKEN")
if not token:
    print("ERROR: GH_TOKEN ist nicht gesetzt.", file=sys.stderr)
    sys.exit(1)

# GitHub API-Call
api_url = f"https://api.github.com/repos/{REPO}/releases/latest"
headers = {"Authorization": f"token {token}"}
res = requests.get(api_url, headers=headers)

# Fehler bei nicht-200
if res.status_code != 200:
    print(f"ERROR: GitHub API returned {res.status_code}\n{res.text}", file=sys.stderr)
    sys.exit(1)

data = res.json()

# Prüfen, ob wir ein Release bekommen haben
if "tag_name" not in data:
    print("ERROR: Keine gültigen Release-Daten erhalten.", file=sys.stderr)
    sys.exit(1)

# Version extrahieren
tag = data["tag_name"]
version = data.get("name", tag)

# IPA suchen
ipa_url = None
size = 0
for asset in data.get("assets", []):
    if asset.get("name", "").lower().endswith(".ipa"):
        ipa_url = asset["browser_download_url"]
        size = asset.get("size", 0)
        break

if not ipa_url:
    print("ERROR: Keine .ipa-Datei im Release gefunden!", file=sys.stderr)
    sys.exit(1)

# JSON bauen
json_data = {
    "name": "YTLite",
    "identifier": "com.savagefrvr.ytlite",
    "subtitle": "Lightweight YouTube app",
    "developer": "SavageFRVR",
    "sourceURL": "https://pre-venti.github.io/ytlite-mizuki-json/ytlite.json",
    "iconURL": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/YouTube_social_white_squircle_%282017%29.svg/200px-YouTube_social_white_squircle_%282017%29.svg.png",
    "tintColor": "#FF0000",
    "apps": [{
        "name": "YTLite",
        "bundleIdentifier": "com.savagefrvr.ytlite",
        "version": version,
        "developerName": "SavageFRVR",
        "subtitle": "YouTube ohne Werbung und Tracking",
        "downloadURL": ipa_url,
        "iconURL": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/YouTube_social_white_squircle_%282017%29.svg/200px-YouTube_social_white_squircle_%282017%29.svg.png",
        "localizedDescription": "Ein modifizierter YouTube-Client mit Fokus auf Minimalismus und Datenschutz.",
        "size": size,
        "versionDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "versionDescription": data.get("body", ""),
        "tintColor": "#FF0000"
    }]
}

# Datei schreiben
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)

print(f"{OUTPUT_FILE} erfolgreich generiert (Version {version}).")
