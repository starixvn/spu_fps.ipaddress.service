from flask import jsonify

def invalid_ip_response(ip_address):
    return jsonify({"error": f"Invalid xActual_IP: {ip_address}"}), 400

def success_response(ip_address, is_actual_ip=False, details=None, ip_list=None):
    response = {"status": "success", "is_actual_ip": is_actual_ip}
    if not is_actual_ip:
        response["verified_ip"] = ip_address
    if details:
        response.update(details)
    if ip_list:
        response["ip_list"] = ip_list

    return jsonify(response)

def failed_response(reason="No valid IP found"):
    return jsonify({"status": "failed", "message": reason}), 404
