import firebase_admin
from firebase_admin import credentials, db
from src.config import FIREBASE_URL

def init_database():
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_URL})
    return db

db = init_database()