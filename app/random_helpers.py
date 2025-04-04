import requests

def fetch_instance_ip():
    try:
        return "Unable to retrieve public IP"
        #return requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").text
    except requests.RequestException:
        return "Unable to retrieve public IP"