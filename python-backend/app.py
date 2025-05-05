from flask import Flask
from flask_cors import CORS
from endpoints.auth import auth_bp
from endpoints.sensor_data import sensor_data_bp
from endpoints.gps_data import geo_data_bp

from dotenv import load_dotenv
import os
import json

load_dotenv
with open('secret-key.json') as f:
    secret_key= json.load(f)['SECRET_KEY']
    
app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(sensor_data_bp, url_prefix='/api/v1/sensor')
app.register_blueprint(geo_data_bp, url_prefix='/api/v1/geo')
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)