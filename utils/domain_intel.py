import whois
import ssl
import socket
import tldextract
from datetime import datetime

def get_domain(url):
    ext = tldextract.extract(url)
    return ext.registered_domain

def domain_age_score(url):
    try:
        domain = get_domain(url)
        w = whois.whois(domain)

        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]

        if not creation:
            return 2

        age_days = (datetime.now() - creation).days

        if age_days > 365 * 5:
            return -2
        elif age_days > 365:
            return -1
        elif age_days > 180:
            return 0
        else:
            return 2

    except:
        return 2

def ssl_score(url):
    try:
        domain = get_domain(url)

        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=3) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

                issuer = cert.get("issuer")
                if issuer:
                    return -2
                else:
                    return 1
    except:
        return 2
