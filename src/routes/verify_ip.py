from flask import request
from responses.custom_responses import invalid_ip_response, success_response, failed_response
from utils.ip_helpers import get_valid_ips, save_all_valid_ips, is_valid_ip, get_ip_info_from_db
from utils.ip_utils import validate_ip, get_ip_info

def verify_ip_endpoint():
    # Get the X-Actual-IP and X-Forwarded-For headers from the request
    x_actual_ip = request.headers.get("X-Actual-IP")
    x_forward_ips = request.headers.get("X-Forwarded-For", "")

    # Validate the actual IP address
    if not validate_ip(x_actual_ip):
        return invalid_ip_response(x_actual_ip)

    # Split and clean the forwarded IPs
    if x_forward_ips:
        x_forward_ips = [ip.strip() for ip in x_forward_ips.split(",")]

    # Ensure the actual IP is included in the forwarded IPs list
    if x_actual_ip not in x_forward_ips:
        x_forward_ips.insert(0, x_actual_ip)

    ip_info_cache = {}
    for ip in x_forward_ips:
        # Check IP info from the database or API
        ip_info = get_ip_info_from_db(ip)
        if ip_info is None:
            ip_info = get_ip_info(ip)
        ip_info_cache[ip] = ip_info

    # Get the list of valid IPs from the forwarded IPs
    valid_ips = get_valid_ips(x_forward_ips, ip_info_cache)

    # Save all valid IPs to the database
    save_all_valid_ips(x_forward_ips, ip_info_cache)

    # Check if the actual IP is valid and not a VPN, CDN, or proxy
    if is_valid_ip(x_actual_ip, valid_ips, ip_info_cache):
        return success_response(x_actual_ip, is_actual_ip=True)

    # If the actual IP is not valid, use a valid IP from the forwarded IPs
    for ip in valid_ips:
        if is_valid_ip(ip, valid_ips, ip_info_cache):
            return success_response(ip, is_actual_ip=False)

    # If no valid IP is found, return a failed response
    return failed_response()