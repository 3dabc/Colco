import firebase_admin
from firebase_admin import credentials, firestore
import os

service_account_path = os.getenv(GOOGLE_APPLICATION_CREDENTIALS)
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)
db = firestore.client()