import geoip2.database

from utils.ip_threat_detector import is_private_ip
from utils.ip_utils import get_ip_info

# TODO: Filter out private IP addresses from the list
def filter_private_ips(ip_list):
    """Filter out private IP addresses from the list."""
    return [ip for ip in ip_list if not is_private_ip(ip)]

def get_geolocation(ip, geoip_db_path):
    """Get geolocation information for an IP address."""
    reader = geoip2.database.Reader(geoip_db_path)
    try:
        response = reader.city(ip)
        location = {
            'ip': ip,
            'country': response.country.iso_code,
            'region': response.subdivisions.most_specific.iso_code,
            'city': response.city.name,
            'latitude': response.location.latitude,
            'longitude': response.location.longitude,
            'timezone': response.location.time_zone
        }
    except geoip2.errors.AddressNotFoundError:
        location = {
            'ip': ip,
            'country': None,
            'region': None,
            'city': None,
            'latitude': None,
            'longitude': None,
            'timezone': None
        }
    reader.close()
    return location

def get_locations_for_ips(x_forward_ips, geoip_db_path):
    """Get geolocation information for each IP in x_forward_ips if there are two or more IPs."""
    x_forward_ips = filter_private_ips(x_forward_ips)
    if len(x_forward_ips) >= 2:
        return [get_geolocation(ip, geoip_db_path) for ip in x_forward_ips]
    return []

def find_ips_with_matching_timezone(locations, request_timezone):
    """Find the IPs with a matching timezone and check for proxy or VPN usage."""
    matching_ips = [location['ip'] for location in locations if location['timezone'] == request_timezone]
    
    if len(matching_ips) >= 2:
        # Perform additional checks to find IPs using proxy or VPN
        matching_ips = [ip for ip in matching_ips if not is_using_proxy_or_vpn(ip)]
    
    return matching_ips[0] if matching_ips else None

def is_using_proxy_or_vpn(ip):
    """Check if an IP is using a proxy or VPN."""
    ip_info = get_ip_info(ip)
    return ip_info.get('proxy') == 'yes' and ip_info.get('type') == 'VPN'