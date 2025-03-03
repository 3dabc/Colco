from flask import Flask
from endpoints.auth import auth_bp
from endpoints.sensor_data import sensor_data_bp
from endpoints.geo_data import geo_data_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sensor_data_bp)
app.register_blueprint(geo_data_bp)

if __name__ == '__main__':
    app.run(debug=True)