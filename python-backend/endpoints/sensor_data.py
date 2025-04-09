from flask import Blueprint, jsonify, request
from firebase_admin import auth

sensor_data_bp = Blueprint('sensor_data', __name__)

# Mock data for light intensity and soil moisture
sensor_data = {
    "light_intensity": 50000,  # Example value
    "soil_moisture": 75  # Example value
}

# Route to get sensor data
@sensor_data_bp.route('/api/v1/sensor/<user_id>', methods=['GET'])
def get_sensor_data():
    token = request.headers.get('Authorization')
    try:
        auth.get_account_info(token)
        return jsonify(sensor_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401


# This route should be used to update the sensor data manually via the frontend
@sensor_data_bp.route('/api/v1/sensor/<user_id>/update', methods=['POST'])
def update_sensor_data(user_id):
    token = request.headers.get('Authorization')
    try:
        auth.get_account_info(token)
        data = request.json
        # Update the mock data with the new values from the request
        sensor_data.update(data)
        return jsonify({"message": "Sensor data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401