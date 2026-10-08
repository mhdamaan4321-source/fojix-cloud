from flask import Flask, jsonify, request
from nacl.public import PrivateKey
import base64

app = Flask(__name__)

def generate_wireguard_keys():
    """Real WireGuard Private & Public key pair generate seiyum function"""
    private_key_obj = PrivateKey.generate()
    public_key_obj = private_key_obj.public_key

    # Keys-ai base64 format-ukku encode seidhal
    private_key = base64.b64encode(bytes(private_key_obj)).decode('ascii')
    public_key = base64.b64encode(bytes(public_key_obj)).decode('ascii')

    return private_key, public_key

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "service": "Fojix VPN Backend API",
        "version": "1.0.0"
    }), 200

@app.route('/api/vpn/generate-keys', methods=['POST'])
def get_keys():
    try:
        priv_key, pub_key = generate_wireguard_keys()
        return jsonify({
            "success": True,
            "private_key": priv_key,
            "public_key": pub_key
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/vpn/connect', methods=['POST'])
def connect_vpn():
    data = request.get_json() or {}
    user_id = data.get("user_id", "anonymous")

    priv_key, pub_key = generate_wireguard_keys()
    
    # User-ukkaana WireGuard configuration format
    wg_config = f"""[Interface]
PrivateKey = {priv_key}
Address = 10.0.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY_HERE
Endpoint = vpn.fojix.cloud:51820
AllowedIPs = 0.0.0.0/0
"""

    return jsonify({
        "success": True,
        "message": f"Connection initialized for user {user_id}",
        "public_key": pub_key,
        "config": wg_config
    }), 200

@app.route('/api/vpn/disconnect', methods=['POST'])
def disconnect_vpn():
    data = request.get_json() or {}
    user_id = data.get("user_id", "anonymous")
    return jsonify({
        "success": True,
        "message": f"User {user_id} disconnected successfully"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)