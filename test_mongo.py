from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["research_db"]

collection = db["test_collection"]

collection.insert_one({
    "message": "MongoDB connected successfully"
})

print("Connected successfully!")