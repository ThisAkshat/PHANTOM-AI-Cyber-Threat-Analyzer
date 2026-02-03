import requests
import socket

ABUSE_API = "https://api.abuseipdb.com/api/v2/check"

# Put your own API key here later (we'll add it)
ABUSE_KEY = ""

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def abuse_score(ip):
    if not ip:
        return 0

    if not ABUSE_KEY:
        return 0   # fallback if no key yet

    headers = {
        "Key": ABUSE_KEY,
        "Accept": "application/json"
    }

    try:
        r = requests.get(
            ABUSE_API,
            headers=headers,
            params={"ipAddress": ip, "maxAgeInDays": 90},
            timeout=10
        )
        data = r.json()["data"]
        return int(data["abuseConfidenceScore"]) / 20
    except:
        return 0
