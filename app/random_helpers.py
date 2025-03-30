import requests

def fetch_instance_ip():
    try:
        public_ipv4 = "Unable to retrieve public IP"
        #public_ipv4 = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").text
    except requests.RequestException:
        public_ipv4 = "Unable to retrieve public IP"