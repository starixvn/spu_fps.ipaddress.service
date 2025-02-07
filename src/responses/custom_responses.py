from flask import jsonify

def invalid_ip_response(ip_address):
    return jsonify({"error": f"Invalid xActual_IP: {ip_address}"}), 400

def success_response(ip_address, is_actual_ip=False, **kwargs):
    response = {
        "is_actual_ip": is_actual_ip,
        "status": "success",
        "verified_ip": ip_address
    }

    response.update({key: value for key, value in kwargs.items() if value})

    return jsonify(response)

def failed_response(reason="No valid IP found"):
    return jsonify({"status": "failed", "message": reason}), 404
