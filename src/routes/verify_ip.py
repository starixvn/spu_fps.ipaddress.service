import ipaddress
from flask import request
from responses import failed_response, success_response
from utils import filter_private_ips, find_ips_with_matching_timezone, get_locations_for_ips
from utils.ip_utils import filter_ipv4_addresses, validate_ip_list

GEOIP_DB_PATH = 'src/data/GeoLite2-City.mmdb'

def get_ip_headers():
    return {
        "actual_ip": request.headers.get("X-Actual-IP"),
        "forwarded_ips": request.headers.get("X-Forwarded-For"),
        "originating_ip": request.headers.get("X-Originating-IP"),
        "remote_ip": request.headers.get("X-Remote-IP"),
        "remote_addr": request.headers.get("X-Remote-Addr"),
        "timezone": request.headers.get("timezone"),
    }

def parse_ip_list(headers):
    ip_list = [
        headers["originating_ip"], 
        headers["remote_ip"], 
        headers["remote_addr"]
    ]
    if headers["forwarded_ips"]:
        ip_list.extend(ip.strip() for ip in headers["forwarded_ips"].split(","))
    return ip_list  

def count_ip_occurrences(ip_list, target_ip):
    return ip_list.count(target_ip)

def build_ip_response(actual_ip, matching_ips, locations, ip_list):
    if actual_ip == matching_ips[0]:
        return success_response(actual_ip, is_actual_ip=True)

    details = next((loc for loc in locations if loc["ip"] == matching_ips[0]), {})
    potential_ips = matching_ips if len(matching_ips) >= 2 else None
    return success_response(matching_ips[0], is_actual_ip=False, details=details, ip_list=ip_list, potential_ips=potential_ips)

def verify_ip_endpoint():
    headers = get_ip_headers()
    ip_list = parse_ip_list(headers)
    actual_ip_count = count_ip_occurrences(ip_list, headers["actual_ip"])

    ip_list = list(filter(None, set(ip_list)))
    ip_list = validate_ip_list(headers["actual_ip"], ip_list)
    if isinstance(ip_list, tuple):  
        return ip_list

    forwarded_ips = [ip.strip() for ip in headers["forwarded_ips"].split(",")] if headers["forwarded_ips"] else []

    if actual_ip_count < 2 or headers["actual_ip"] not in forwarded_ips:

        # FEATURE: Backend will handle actual IP proof verification in the future.
        locations = get_locations_for_ips(ip_list, GEOIP_DB_PATH)
        matching_ips = find_ips_with_matching_timezone(locations, headers["timezone"])
        
        if matching_ips:
            return build_ip_response(headers["actual_ip"], matching_ips, locations, ip_list)
        
        return failed_response("No matching IP found")
        
    return success_response(headers["actual_ip"], is_actual_ip=True)
