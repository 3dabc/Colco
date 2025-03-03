from flask import Blueprint, jsonify, request
import pyrebase
from .firebase_config import auth

auth_bp = Blueprint('auth', __name__)

# Firebase config
firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "databaseURL": "YOUR_DATABASE_URL",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID",
    "measurementId": "YOUR_MEASUREMENT_ID"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Route for Firebase authentication
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return jsonify({"token": user['idToken']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401