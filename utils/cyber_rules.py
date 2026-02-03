import re

phishing_keywords = [
    "verify", "account", "password", "bank", "login", "click",
    "urgent", "security", "locked", "confirm", "suspended"
]

def keyword_score(text):
    score = 0
    for word in phishing_keywords:
        if word in text.lower():
            score += 1
    return score

def url_score(text):
    urls = re.findall(r'https?://\S+', text)
    if len(urls) > 0:
        return 2
    return 0
