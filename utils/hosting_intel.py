import requests

BAD_ASNS = {
    "13335",   # Cloudflare abused hosting
    "9009",    # M247 (bulletproof hosting)
    "20473",   # Choopa / Vultr (frequently abused)
    "16276",   # OVH abused
    "24940"    # Hetzner abused
}

def get_asn(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        return r.json().get("org", "")
    except:
        return ""

def asn_risk(ip):
    org = get_asn(ip)
    for asn in BAD_ASNS:
        if asn in org:
            return 2
    return 0
