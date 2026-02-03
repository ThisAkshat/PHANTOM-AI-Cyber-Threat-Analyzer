import requests
import time

PHISH_URL = "https://openphish.com/feed.txt"

_cache = {
    "data": set(),
    "last_update": 0
}

def fetch_phish_feed():
    try:
        r = requests.get(PHISH_URL, timeout=10)
        urls = set(r.text.splitlines())
        return urls
    except:
        return set()

def get_phish_urls():
    now = time.time()
    if now - _cache["last_update"] > 1800 or not _cache["data"]:
        _cache["data"] = fetch_phish_feed()
        _cache["last_update"] = now
    return _cache["data"]

def is_known_phish(url):
    feed = get_phish_urls()
    for bad in feed:
        if bad in url:
            return True
    return False
