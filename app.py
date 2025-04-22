import os
import time
import jwt
from flask import Flask, jsonify

# Configuration
role = os.getenv("PGRST_JWT_ROLE")
audience = os.getenv("PGRST_JWT_AUD")
expires_in = int(os.getenv("PGRST_JWT_EXPIRE_TIME", 3600))  # Default to 3600 (1 hour) if not set
secret = os.getenv("PGRST_JWT_SECRET")

app = Flask(__name__)

@app.route('/generate-jwt', methods=['GET'])
def generate_jwt():
    if not secret:
        return jsonify({"error": "PGRST_JWT_SECRET not set in environment"}), 500
    if not role or not audience:
        return jsonify({"error": "PGRST_JWT_ROLE or PGRST_JWT_AUD not set in environment"}), 400

    payload = {
        "role": role,
        "aud": audience,
        "exp": int(time.time()) + expires_in
    }

    token = jwt.encode(payload, secret, algorithm="HS256")

    return jsonify({
        "jwt_token": token,
        "expires_at": time.ctime(payload["exp"])
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

