import re
import tldextract
import validators

suspicious_tlds = ["ru", "tk", "ml", "ga", "cf"]

shorteners = ["bit.ly", "tinyurl", "goo.gl", "t.co", "is.gd"]

def extract_urls(text):
    return re.findall(r'https?://\S+', text)

def analyze_url(url):
    score = 0

    if not validators.url(url):
        score += 2

    for s in shorteners:
        if s in url:
            score += 3

    ext = tldextract.extract(url)
    if ext.suffix in suspicious_tlds:
        score += 2

    if url.count("https") > 1:
        score += 2

    if len(url) > 75:
        score += 1

    return score