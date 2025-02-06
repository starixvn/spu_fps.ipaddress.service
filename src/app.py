from flask import Flask
from routes import verify_ip_endpoint

app = Flask(__name__)

# Register routes
app.add_url_rule('/verify-ip', 'verify_ip_endpoint', verify_ip_endpoint, methods=['POST'])

if __name__ == "__main__":
    app.run(debug=True)