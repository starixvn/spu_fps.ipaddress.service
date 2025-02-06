import ipaddress

# List of private IP ranges
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv4Network("127.0.0.0/8"),
    ipaddress.IPv4Network("0.0.0.0/8")
]

# List of specific IP addresses to be treated as private
SPECIFIC_PRIVATE_IPS = [
    ipaddress.IPv4Address("1.1.1.1"),
    ipaddress.IPv4Address("8.8.8.8"),
    ipaddress.IPv4Address("9.9.9.9")
]

def is_private_ip(ip):
    """Check if the IP address is in a private range or a specific private IP."""
    try:
        ip_addr = ipaddress.ip_address(ip)
        return any(ip_addr in net for net in PRIVATE_IP_RANGES) or ip_addr in SPECIFIC_PRIVATE_IPS
    except ValueError:
        return False


