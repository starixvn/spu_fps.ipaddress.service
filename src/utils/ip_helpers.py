from utils.ip_utils import validate_ip
from models import IPInfo, SessionLocal
from config import SPECIAL_IPS
from datetime import datetime, timezone

def get_valid_ips(x_forward_ips, ip_info_cache):
    return [
        ip for ip in x_forward_ips
        if ip not in SPECIAL_IPS and validate_ip(ip) and ip_info_cache[ip] and ip_info_cache[ip] != {}
    ]

def save_all_valid_ips(x_forward_ips, ip_info_cache):
    for ip in x_forward_ips:
        if ip not in SPECIAL_IPS and validate_ip(ip) and ip_info_cache[ip] and ip_info_cache[ip] != {}:
            save_ip_info(ip, ip_info_cache[ip])

def is_valid_ip(ip, valid_ips, ip_info_cache):
    ip_info = ip_info_cache[ip]
    if ip in valid_ips and ip_info.get('proxy') != 'yes' and ip_info.get('type') != 'VPN':
        return True
    return False

def get_ip_info_from_db(ip_address):
    db = SessionLocal()
    try:
        ip_info = db.query(IPInfo).filter(IPInfo.ip_address == ip_address).first()
        if ip_info:
            return {
                'asn': ip_info.asn,
                'range': ip_info.ip_range,
                'provider': ip_info.provider,
                'organisation': ip_info.organisation,
                'continent': ip_info.continent,
                'continentcode': ip_info.continent_code,
                'country': ip_info.country,
                'isocode': ip_info.iso_code,
                'region': ip_info.region,
                'regioncode': ip_info.region_code,
                'timezone': ip_info.timezone,
                'city': ip_info.city,
                'latitude': ip_info.latitude,
                'longitude': ip_info.longitude,
                'currency': ip_info.currency,
                'devices': ip_info.devices,
                'proxy': ip_info.proxy,
                'type': ip_info.ip_type,
                'checked_at': ip_info.checked_at
            }
    finally:
        db.close()
    return None

def save_ip_info(ip_address, info):
    db = SessionLocal()
    try:
        existing_ip_info = db.query(IPInfo).filter(IPInfo.ip_address == ip_address).first()
        if existing_ip_info is None:
            ip_info = IPInfo(
                ip_address=ip_address,
                asn=info.get('asn'),
                ip_range=info.get('range'),
                provider=info.get('provider'),
                organisation=info.get('organisation'),
                continent=info.get('continent'),
                continent_code=info.get('continentcode'),
                country=info.get('country'),
                iso_code=info.get('isocode'),
                region=info.get('region'),
                region_code=info.get('regioncode'),
                timezone=info.get('timezone'),
                city=info.get('city'),
                latitude=info.get('latitude'),
                longitude=info.get('longitude'),
                currency=info.get('currency'),
                devices=info.get('devices'),
                proxy=info.get('proxy'),
                ip_type=info.get('type'),
                checked_at=datetime.now(timezone.utc)
            )
            db.add(ip_info)
            db.commit()
            db.refresh(ip_info)
    finally:
        db.close()