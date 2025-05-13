from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)

# Koneksi ke MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-service:27017")
client = MongoClient(MONGO_URI)
db = client.smart_home
users_collection = db.users

@app.route('/')
def index():
    return jsonify({"message": "Auth Service Connected to MongoDB"}), 200

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    auth_type = data.get("type")        # 'fingerprint' atau 'rfid'
    user_id = data.get("id")            # ID unik dari fingerprint atau RFID

    if not auth_type or not user_id:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    # Cari user berdasarkan tipe autentikasi dan ID
    user = users_collection.find_one({"auth_type": auth_type, "user_id": user_id})

    if user:
        return jsonify({
            "status": "authorized",
            "user_id": user["user_id"],
            "name": user.get("name"),
            "role": user.get("role"),
            "type": auth_type,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }), 200
    else:
        return jsonify({
            "status": "unauthorized",
            "user_id": user_id,
            "type": auth_type,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
