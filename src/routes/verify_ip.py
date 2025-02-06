import ipaddress
from flask import request
from responses.custom_responses import failed_response, invalid_ip_response, success_response
from utils.geoip_utils import filter_private_ips, find_ips_with_matching_timezone, get_locations_for_ips
from utils.ip_utils import validate_ip

# TODO: Extract the X-Actual-IP, X-Forwarded-For, and timezone from the request body
def extract_ip_headers():
    """Extract the X-Actual-IP, X-Forwarded-For, and timezone from the request body."""
    try:
        data = request.get_json()  # Get JSON data from the request body
        x_actual_ip = data.get("x_actual_ip")
        x_forward_ips = data.get("x_forward_ips")
        timezone = data.get("timezone")
    except Exception as e:
        print(f"Error parsing JSON body: {e}")
        x_actual_ip, x_forward_ips, timezone = None, None, None

    return x_actual_ip, x_forward_ips, timezone

# TODO: Validate the actual IP and clean the forwarded IPs
def validate_and_clean_ips(x_actual_ip, x_forward_ips):
    """Validate the actual IP and clean the forwarded IPs."""
    if not validate_ip(x_actual_ip):
        return invalid_ip_response(x_actual_ip)

    if x_forward_ips:
        x_forward_ips = [ip.strip() for ip in x_forward_ips.split(",")]

    return x_forward_ips

# TODO: Filter out IPv6 addresses from the list
def filter_ipv6_addresses(ip_list):
    """Filter out IPv6 addresses from the list."""
    return [ip for ip in ip_list if ipaddress.ip_address(ip).version == 4]

def verify_ip_endpoint():
    x_actual_ip, x_forward_ips, timezone = extract_ip_headers()

    x_forward_ips = validate_and_clean_ips(x_actual_ip, x_forward_ips)
    print(x_forward_ips, x_actual_ip)
    if x_actual_ip not in x_forward_ips:
        if isinstance(x_forward_ips, tuple):  # Check if invalid_ip_response was returned
            return x_forward_ips
        
        x_forward_ips = filter_ipv6_addresses(x_forward_ips)
        x_forward_ips = filter_private_ips(x_forward_ips)

        # Get geolocation information for each IP in x_forward_ips if there are two or more IPs
        geoip_db_path = 'src/data/GeoLite2-City.mmdb'
        locations = get_locations_for_ips(x_forward_ips, geoip_db_path)

        # Find the IP with a matching timezone
        matching_ip = find_ips_with_matching_timezone(locations, timezone)
        if matching_ip:
            return success_response(matching_ip, is_actual_ip=False)
        else:
            return failed_response(reason="No matching IP found with the same timezone")
        
    return success_response(x_actual_ip, is_actual_ip=True)