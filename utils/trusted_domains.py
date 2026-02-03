TRUSTED_DOMAINS = [
    "google.com",
    "github.com",
    "leetcode.com",
    "microsoft.com",
    "openai.com",
    "jetbrains.com",
    "stackoverflow.com",
    "amazon.com",
    "apple.com",
    "facebook.com",
    "twitter.com",
    "linkedin.com"
]

def is_trusted_domain(url):
    for d in TRUSTED_DOMAINS:
        if d in url.lower():
            return True
    return False
