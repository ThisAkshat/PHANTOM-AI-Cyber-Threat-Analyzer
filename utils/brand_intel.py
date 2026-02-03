import re

# Real brands attackers love to impersonate
BRANDS = [
    "google", "facebook", "amazon", "apple", "microsoft", "paypal",
    "bankofamerica", "icici", "hdfc", "sbi", "instagram", "netflix",
    "flipkart", "phonepe", "gpay", "whatsapp", "linkedin", "github",
    "naukri", "myntra", "airtel", "jio", "swiggy", "zomato"
]

# Legitimate domains of those brands
OFFICIAL_DOMAINS = {
    "amazon": ["amazon.com", "amazon.in"],
    "google": ["google.com"],
    "facebook": ["facebook.com"],
    "apple": ["apple.com"],
    "microsoft": ["microsoft.com"],
    "paypal": ["paypal.com"],
    "bankofamerica": ["bankofamerica.com"],
    "icici": ["icicibank.com"],
    "hdfc": ["hdfcbank.com"],
    "sbi": ["sbi.co.in"],
    "instagram": ["instagram.com"],
    "netflix": ["netflix.com"],
    "flipkart": ["flipkart.com"],
    "github": ["github.com"],
    "naukri": ["naukri.com"]
}

SUSPICIOUS_TLDS = [
    ".xyz", ".top", ".work", ".click", ".loan", ".gq", ".cf", ".tk",
    ".ml", ".buzz", ".monster", ".support", ".review", ".zip"
]

def brand_spoof_score(domain):
    domain = domain.lower()
    score = 0

    for brand in BRANDS:
        if brand in domain:
            legit = OFFICIAL_DOMAINS.get(brand, [])

            # If domain is NOT one of the official ones → brand abuse
            if not any(domain.endswith(d) for d in legit):
                score += 4

    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score += 2

    # Detect tricks like bankofamerica-login-secure[.]com
    if re.search(r"(login|verify|secure|update|account|billing)", domain):
        score += 2

    return score
