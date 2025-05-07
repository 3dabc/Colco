from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from firebase_config import db
import logging

account_bp = Blueprint('account', __name__)

# Route for getting account information
@account_bp.route('/api/v1/account/<user_id>', methods=['GET'])
@cross_origin()
def get_account(user_id):
    try:
        user = db.collection('users').document(user_id).get()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        logging.error(e)
        return jsonify({"error": str(e)}), 401

# Route for deleting an account
@account_bp.route('/api/v1/account/<user_id>/delete', methods=['DELETE'])
@cross_origin()
def delete_account(user_id):
    try:
        db.collection('users').document(user_id).delete()
        return jsonify({'message':'Account deleted'}), 200
    except Exception as e:
        logging.error(e)
        return jsonify({"error": str(e)}), 401
    
# Route for updating account information - Needs to be tested and reworked to properly interact with the front end
@account_bp.route('/api/v1/account/<user_id>/update', methods=['PUT'])
@cross_origin()
def update_account(user_id):
    try:
        data = request.json
        db.collection('users').document(user_id).update(data)
        return jsonify({'message':'Account updated'}), 200
    except Exception as e:
        logging.error(e)
        return jsonify({"error": str(e)}), 401
    
    