import random
import datetime
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firestore
def initialize_firestore():
    # Path to your service account key
    service_account_path = 'python-backend/secret-key.json'  # Update this path if needed
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)
    return firestore.client()

# Generate realistic sensor data
def generate_fake_sensor_data(timestamp, latitude, longitude):
    data = {
        "timestamp": timestamp.isoformat(),
        "soil_moisture": round(random.uniform(10, 60), 2),  # Percentage (10% - 60%)
        "soil_ph": round(random.uniform(6.0, 7.5), 2),  # Neutral to slightly alkaline
        "temperature": round(random.uniform(15, 35), 2),  # Celsius (15°C - 35°C)
        "gps_coordinates": {"latitude": latitude, "longitude": longitude},
        "light_intensity": random.randint(10000, 80000)  # Lux (10,000 - 80,000)
    }
    return data

# Generate and store data in Firestore
def generate_and_store_data(db, user_id):
    # Northridge, CA coordinates
    latitude = 34.245678
    longitude = -118.520123

    # Start time: 7 days ago
    start_time = datetime.datetime.now() - datetime.timedelta(days=7)
    end_time = datetime.datetime.now()

    # Firestore collection reference
    node_id = f"node {user_id}"  # Example: "node 1"
    collection_ref = db.collection('colco-db').document('colco-testing').collection(node_id)

    # Generate data for every 5 minutes
    current_time = start_time
    while current_time <= end_time:
        fake_data = generate_fake_sensor_data(current_time, latitude, longitude)
        collection_ref.add(fake_data)  # Add data to Firestore
        current_time += datetime.timedelta(minutes=5)  # Increment by 5 minutes

    print(f"Data for the last 7 days has been generated and stored for {node_id}.")

if __name__ == "__main__":
    # Initialize Firestore
    db = initialize_firestore()

    # Replace with the desired user ID
    user_id = 1
    generate_and_store_data(db, user_id)