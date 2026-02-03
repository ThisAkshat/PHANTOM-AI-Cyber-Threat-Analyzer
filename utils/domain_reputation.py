HIGH_TRUST = [
    "google.com",
    "microsoft.com",
    "amazon.com",
    "linkedin.com",
    "naukri.com",
    "leetcode.com",
    "github.com",
    "apple.com",
    "facebook.com",
    "openai.com"
]

def domain_trust(url):
    for d in HIGH_TRUST:
        if d in url.lower():
            return -3
    return 0
