from flask import Blueprint, jsonify, request
import pyrebase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

auth_bp = Blueprint('auth', __name__)

# Firebase config using environment variables
firebase_config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID')
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