from flask import Blueprint, jsonify, request
from firebase_admin import auth
from firebase_config import db 
import logging

sensor_data_bp = Blueprint('sensor_data', __name__)

# Mock data for light intensity and soil moisture
sensor_data = {
    "light_intensity": 50000,  # Example value
    "soil_moisture": 75  # Example value
}

# Route to get sensor data
@sensor_data_bp.route('/<user_id>', methods=['GET'])
def get_sensor_data(user_id):
    token = request.headers.get('Authorization')
    try:
        if not token:
            raise ValueError("Authorization token is missing")

        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token.split("Bearer ")[1]

        # Verify the token
        decoded_token = auth.verify_id_token(token)
        logging.info(f"Decoded token: {decoded_token}")

        node_id = f"node {user_id}"
        logging.info(f"Fetching data for node_id: {node_id}")
        collection_ref = db.collection('colco-db').document('colco-testing').collection(node_id)
        docs = collection_ref.stream()

        # Extract data
        sensor_data_list = [doc.to_dict() for doc in docs]
        logging.info(f"Fetched {len(sensor_data_list)} documents for node_id: {node_id}")

        if not sensor_data_list:
            return jsonify({"message": "No sensor data found for this user"}), 404

        # Initialize sums and counts for averaging
        total_soil_moisture = 0
        total_relative_humidity = 0
        total_temperature = 0
        total_light_intensity = 0
        total_soil_ph = 0
        count = 0

        for data in sensor_data_list:
            total_soil_moisture += data.get("soil_moisture", 0)
            total_relative_humidity += data.get("relative_humidity", 0)
            total_temperature += data.get("temperature", 0)
            total_light_intensity += data.get("light_intensity", 0)
            total_soil_ph += data.get("soil_ph", 0)
            count += 1

        # Calculate averages
        averages = {
            "soilMoisture": round(total_soil_moisture / count, 2) if count > 0 else "N/A",
            "relativeHumidity": round(total_relative_humidity / count, 2) if count > 0 else "N/A",
            "temperature": round(total_temperature / count, 2) if count > 0 else "N/A",
            "lightIntensity": round(total_light_intensity / count, 2) if count > 0 else "N/A",
            "soilPH": round(total_soil_ph / count, 2) if count > 0 else "N/A",
        }

        # Return both averages and original dataset
        return jsonify({
            "avg": averages,
            "data": sensor_data_list
        }), 200
    except Exception as e:
        logging.error(f"Error in get_sensor_data: {e}")
        return jsonify({"error": str(e)}), 500

# This route should be used to update the sensor data manually via the frontend
@sensor_data_bp.route('/<user_id>/update', methods=['POST'])
def update_sensor_data(user_id):
    token = request.headers.get('Authorization')
    try:
        auth.get_account_info(token)
        data = request.json

        # Update the mock data with the new values from the request
        sensor_data.update(data)

        # Add data to Firestore
        node_id = f"node {user_id}"  # Example: "node 1"
        collection_ref = db.collection('colco-db').document('colco-testing').collection(node_id)
        document_data = {
            "timestamp": data.get("timestamp"),
            "soil_moisture": data.get("soil_moisture"),
            "soil_ph": data.get("soil_ph"),
            "temperature": data.get("temperature"),
            "gps_coordinates": data.get("gps_coordinates"),
            "light_intensity": data.get("light_intensity"),
        }
        collection_ref.add(document_data)

        return jsonify({"message": "Sensor data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401