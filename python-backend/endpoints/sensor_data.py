from flask import Blueprint, jsonify, request
from firebase_admin import auth

sensor_data_bp = Blueprint('sensor_data', __name__)

# Mock data for light intensity and soil moisture
sensor_data = {
    "light_intensity": 50000,  # Example value
    "soil_moisture": 75  # Example value
}

# Route to get sensor data
@sensor_data_bp.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    token = request.headers.get('Authorization')
    try:
        auth.get_account_info(token)
        return jsonify(sensor_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401