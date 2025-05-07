from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin
from firebase_config import db
import logging

account_bp = Blueprint('account', __name__)

@account_bp.route('/<user_id>', methods=['OPTIONS', 'GET'])
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def get_account(user_id):
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = make_response('', 200)
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    try:
        # Updated Firestore path for the user document
        user_doc = db.collection('users').document(user_id).get()
        if not user_doc.exists:
            response = jsonify({"error": "User not found"}), 404
        else:
            user_data = user_doc.to_dict()
            response = jsonify(user_data), 200

        # Add CORS headers to the GET response
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    except Exception as e:
        logging.error(f"Error fetching account information for user_id {user_id}: {e}")
        response = jsonify({"error": str(e)}), 500
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

# Route for deleting an account
@account_bp.route('/api/v1/account/<user_id>/delete', methods=['DELETE'])
def delete_account(user_id):
    try:
        # Delete user document from Firestore
        user_doc = db.collection('colco-db').document('colco-testing').collection('users').document(user_id)
        if not user_doc.get().exists:
            return jsonify({"error": "User not found"}), 404

        user_doc.delete()
        return jsonify({'message': 'Account deleted'}), 200
    except Exception as e:
        logging.error(f"Error deleting account for user_id {user_id}: {e}")
        return jsonify({"error": str(e)}), 500

# Route for updating account information
@account_bp.route('/<user_id>/update', methods=['PUT'])
def update_account(user_id):
    try:
        data = request.json

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid data format"}), 400

        # Firestore path for the user document
        user_doc_ref = db.collection('colco-db').document('colco-testing').collection('users').document(user_id)

        # Check if the user document exists
        if not user_doc_ref.get().exists:
            # Create a new user profile if it does not exist
            logging.info(f"User {user_id} does not exist. Creating a new profile.")
            user_doc_ref.set(data)
            return jsonify({'message': 'User profile created successfully'}), 201

        # Update the existing user document with new data
        user_doc_ref.set(data, merge=True)
        return jsonify({'message': 'Account updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating account for user_id {user_id}: {e}")
        return jsonify({"error": str(e)}), 500