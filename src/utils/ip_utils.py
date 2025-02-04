import ipaddress
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv('API_KEY', 'abc-xyz')

def get_ip_info(ip_address):
    url = f'https://proxycheck.io/v2/{ip_address}?vpn=1&asn=1&key={API_KEY}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get(ip_address, {})
        else:
            return {'error': 'Failed to retrieve data', 'status_code': response.status_code}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

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