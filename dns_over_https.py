import requests
from utils import log_info

DOH_SERVER = "https://dns.google/resolve"

def enable_dns_over_https():
    log_info("Enabling DNS-over-HTTPS...")

    domain = "example.com"
    link = f"{DOH_SERVER}?name={domain}&type=A"
    url = link

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "Answer" in data:
            ip_address = data["Answer"][0]["data"]
            log_info(f"Resolved {domain} to {ip_address} via DOH")
        else:
            log_info(f"No DNS record found for {domain} using DOH.")
    except requests.exceptions.RequestException as e:
        log_info(f"Error resolving DNS over HTTPS: {e}")

if __name__ =="__main__":
    enable_dns_over_https()