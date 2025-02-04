from flask import jsonify

def invalid_ip_response(ip_address):
    return jsonify({"error": f"Invalid xActual_IP: {ip_address}"}), 400

def success_response(ip_address, is_actual_ip=False):
    response = {"status": "success", "is_actual_ip": is_actual_ip}
    if not is_actual_ip:
        response["verified_ip"] = ip_address

    return jsonify(response)

def failed_response():
    return jsonify({"status": "failed", "message": "No valid IP found"}), 404
