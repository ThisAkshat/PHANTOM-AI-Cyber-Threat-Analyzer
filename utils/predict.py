import torch
from transformers import BertTokenizer, BertForSequenceClassification

from utils.cyber_rules import keyword_score, url_score
from utils.url_scanner import extract_urls, analyze_url
from utils.domain_reputation import domain_trust
from utils.domain_intel import domain_age_score, ssl_score
from utils.trusted_domains import is_trusted_domain
from utils.threat_intel import is_known_phish
from utils.ip_intel import get_ip, abuse_score
from utils.hosting_intel import asn_risk
from utils.brand_intel import brand_spoof_score

model = BertForSequenceClassification.from_pretrained("model")
tokenizer = BertTokenizer.from_pretrained("model")

labels = ["safe", "phishing"]

def predict(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    )

    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    ml_conf, predicted = torch.max(probs, dim=1)

    ml_label = labels[predicted.item()]
    ml_conf = ml_conf.detach().item()

    urls = extract_urls(text)

    # ============ HARD BLOCK LAYER ============
    # Real phishing feeds
    for u in urls:
        if brand_spoof_score(u) >= 5:
            return "phishing", 0.97

    # Brand spoofing (amazon-login, microsoft-update, etc)
    for u in urls:
        if brand_spoof_score(u) >= 5:
            return "phishing", 0.97
    # =========================================

    # ============ SOFT SCORING LAYER ============
    kw_score = keyword_score(text)
    base_url_score = url_score(text)

    url_risk = 0
    for u in urls:
        url_risk += analyze_url(u)
        url_risk += domain_trust(u)
        url_risk += domain_age_score(u)
        url_risk += ssl_score(u)
        url_risk += brand_spoof_score(u)

        ip = get_ip(u)
        url_risk += abuse_score(ip)
        url_risk += asn_risk(ip)

    cyber = kw_score + base_url_score + url_risk

    # ML thinks safe → reduce paranoia a bit
    if ml_label == "safe":
        cyber -= 2
    # =========================================

    # Trusted brands get protection
    for u in urls:
        if is_trusted_domain(u) and ml_label == "safe":
            return "safe", max(ml_conf, 0.9)
        # ---- Legitimate security notification filter ----
    if ml_label == "safe":
        if "do not click" in text.lower() or "we will never ask" in text.lower():
            cyber -= 3

    if "official" in text.lower() and "https://" in text.lower():
        cyber -= 2


    # Final decision
    if cyber >= 6:
        return "phishing", min(0.97, ml_conf + 0.25)

    return ml_label, ml_conf
