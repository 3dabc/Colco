from flask import Blueprint, jsonify, request
from .firebase_config import auth
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

geo_data_bp = Blueprint('geo_data', __name__)

# Route to get geopositional data and temperature
@geo_data_bp.route('/geo_data', methods=['GET'])
def get_geo_data():
    token = request.headers.get('Authorization')
    try:
        auth.get_account_info(token)
        
        # Replace with actual latitude and longitude values
        latitude = 34.0522
        longitude = -118.2437

        # Get the WeatherAPI key from environment variables
        weather_api_key = os.getenv('WEATHER_API_KEY')

        # Make a request to the WeatherAPI
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={latitude},{longitude}"
        response = requests.get(weather_url)
        weather_data = response.json()

        # Extract temperature from the WeatherAPI response
        temperature = weather_data['current']['temp_c']

        geo_data = {
            "latitude": latitude,
            "longitude": longitude,
            "temperature": temperature
        }
        return jsonify(geo_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401