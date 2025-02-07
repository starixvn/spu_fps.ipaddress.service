import geoip2.database
from geoip2.errors import AddressNotFoundError

from utils.ip_utils import filter_private_ips

def get_geolocation(ip, geoip_db_path):
    try:
        with geoip2.database.Reader(geoip_db_path) as reader:
            response = reader.city(ip)
            return {
                'ip': ip,
                'country': response.country.iso_code,
                'region': response.subdivisions.most_specific.iso_code,
                'city': response.city.name,
                'latitude': response.location.latitude,
                'longitude': response.location.longitude,
                'timezone': response.location.time_zone
            }
    except AddressNotFoundError:
        return {
            'ip': ip,
            'country': None,
            'region': None,
            'city': None,
            'latitude': None,
            'longitude': None,
            'timezone': None
        }
    except Exception as e:
        return {
            'ip': ip,
            'country': None,
            'region': None,
            'city': None,
            'latitude': None,
            'longitude': None,
            'timezone': None
        }

def get_locations_for_ips(x_forward_ips, geoip_db_path):
    x_forward_ips = filter_private_ips(x_forward_ips)
    if len(x_forward_ips) >= 2:
        return [get_geolocation(ip, geoip_db_path) for ip in x_forward_ips]
    return []

def find_ips_with_matching_timezone(locations, request_timezone):
    matching_ips = [location['ip'] for location in locations if location['timezone'] == request_timezone]
    
    return matching_ips if matching_ips else None

# FEATURE: Implement this function in the future.

# def is_using_proxy_or_vpn(ip):
#     ip_info = get_ip_info(ip)
#     if ip_info == {} or ip_info.get('error'):
#         return True
#     return ip_info.get('proxy') == 'yes' or ip_info.get('type') == 'VPN'