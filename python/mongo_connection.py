from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

load_dotenv()

uri = str(os.getenv('MONGO_URI'))

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Establish the database we are using
db = client["youth_group_database"]

event_type_schemas = db["event_type_schemas"]
event_custom_fields = db["event_custom_fields"]

def get_mongo_connection():
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)