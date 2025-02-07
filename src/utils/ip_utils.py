import ipaddress
import requests
import os
from dotenv import load_dotenv

from responses.custom_responses import invalid_ip_response
from utils.ip_threat_detector import is_private_ip

# FEATURE: Implement this function in the future.

# load_dotenv()  # Load environment variables from .env file

# API_KEY = os.getenv('API_KEY', 'abc-xyz')

# def get_ip_info(ip_address):
#     url = f'https://proxycheck.io/v2/{ip_address}?vpn=1&asn=1&key={API_KEY}'
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             return data.get(ip_address, {})
#         else:
#             return {'error': 'Failed to retrieve data', 'status_code': response.status_code}
#     except requests.exceptions.RequestException as e:
#         return {'error': str(e)}

def validate_ip(ip_address: str) -> bool:
    """
    Validate IPv4 address.
    
    Args:
        ip_address (str): IP address to validate.
    
    Returns:
        bool: True if IP address is valid, otherwise False.
    """
    try:
        ipaddress.IPv4Address(ip_address)
        return True
    except ipaddress.AddressValueError:
        return False
    
def filter_ipv4_addresses(ip_list):
    return [ip for ip in ip_list if ipaddress.ip_address(ip).version == 4]

def filter_private_ips(ip_list):
    return [ip for ip in ip_list if not is_private_ip(ip)]

def validate_ip_list(actual_ip, ip_list):
    if not validate_ip(actual_ip):
        return invalid_ip_response(actual_ip)
    ip_list = filter_ipv4_addresses(ip_list)
    ip_list = filter_private_ips(ip_list)
    return ip_list