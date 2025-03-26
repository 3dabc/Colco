from flask import Blueprint, jsonify, request
import requests
import os
from dotenv import load_dotenv
from firebase_admin import auth
from firebase_config import db
    
load_dotenv()

geo_data_bp = Blueprint('geo_data', __name__)

@geo_data_bp.route('/geo_data', methods=['GET'])
def get_geo_data():
    token = request.headers.get('Authorization')
    try:
        auth.get_account_info(token)
        
        # Need to use exact coordinates for where farm is
        # Probabily will make this automatic using the onboard GPS or via google geolocation API
        latitude = 34.0522
        longitude = -118.2437

        # Weather API Jey
        weather_api_key = os.getenv('WEATHER_API_KEY')

        # Request
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={latitude},{longitude}"
        response = requests.get(weather_url)
        weather_data = response.json()

        # Temps from response
        temperature = weather_data['current']['temp_c']

        geo_data = {
            "latitude": latitude,
            "longitude": longitude,
            "temperature": temperature
        }
        return jsonify(geo_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401