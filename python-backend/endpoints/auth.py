from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import pyrebase
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()
logging.basicConfig(level=logging.DEBUG)


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

# FireAuth Routes
    
@auth_bp.route('api/v1/account/<user_id>/update-password', methods=['POST'])
@cross_origin()
def update_password():
    user_id = request.view_args['user_id']
    password = request.json.get('password')
    try:
        auth.update_user(user_id, password=password)
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
@auth_bp.route('api/v1/account/<user_id>/delete', methods=['POST'])
def delete():
    user_id = request.view_args['user_id']
    try:
        auth.delete_user(user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401