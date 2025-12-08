from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

uri = str(os.getenv('MONGO_URI'))

# Create a new client and connect to the server with proper TLS
client = MongoClient(
    uri,
    server_api=ServerApi('1'),
    tlsCAFile=certifi.where()  # Use certifi's CA bundle instead of allowing invalid certs
)

# Establish the database we are using
db = client["youth_group_database"]

# Populate with sample data for demo
event_type_schemas = db["event_type_schemas"]
event_custom_fields = db["event_custom_fields"]

# Data provided by chatgpt
event_type_schemas_data = [
    # Retreat
    {
    "event_type_id": 1,
    "fields": [
        { "name": "packing_list", "type": "text" },
        { "name": "overnight", "type": "boolean" },
        { "name": "num_sessions", "type": "number" }
    ]
    },
    # Worship Night
    {
    "event_type_id": 2,
    "fields": [
        { "name": "theme", "type": "text" },
        { "name": "guest_band", "type": "text" },
        { "name": "is_livestreamed", "type": "boolean" }
    ]
    },
    # Service Project
    {
    "event_type_id": 3,
    "fields": [
        { "name": "location", "type": "text" },
        { "name": "requires_supplies", "type": "boolean" },
        { "name": "hours_expected", "type": "number" }
    ]
    },
    {
    "event_type_id": 4,
    "fields": [
        { "name": "games_planned", "type": "text" },
        { "name": "lights_out_time", "type": "text" },
        { "name": "snacks_provided", "type": "boolean" }
    ]
    },
    # Missions Trip
    {
    "event_type_id": 5,
    "fields": [
        { "name": "destination", "type": "text" },
        { "name": "total_cost", "type": "number" },
        { "name": "passport_required", "type": "boolean" }
    ]
    },
    # Bible Study
    {
    "event_type_id": 6,
    "fields": [
        { "name": "topic", "type": "text" },
        { "name": "chapter_range", "type": "text" },
        { "name": "has_discussion", "type": "boolean" }
    ]
    },
    # Leadership Training
    {
    "event_type_id": 7,
    "fields": [
        { "name": "trainer_name", "type": "text" },
        { "name": "num_modules", "type": "number" },
        { "name": "certificate_awarded", "type": "boolean" }
    ]
    },
    # Fundraiser
    {
    "event_type_id": 8,
    "fields": [
        { "name": "fundraising_goal", "type": "number" },
        { "name": "beneficiary", "type": "text" },
        { "name": "is_online", "type": "boolean" }
    ]
    },
    # Camp Day
    {
    "event_type_id": 9,
    "fields": [
        { "name": "activities", "type": "text" },
        { "name": "waiver_required", "type": "boolean" },
        { "name": "max_capacity", "type": "number" }
    ]
    },
    # Orientation Training
    {
    "event_type_id": 10,
    "fields": [
        { "name": "orientation_leader", "type": "text" },
        { "name": "expected_hours", "type": "number" },
        { "name": "background_check_required", "type": "boolean" }
    ]
    }
]

event_custom_fields_data = [
    # Winter Retreat 2025
    {
    "event_id": 1001,
    "event_type_id": 1,
    "fields": {
        "packing_list": "sleeping bag, toiletries",
        "overnight": True,
        "num_sessions": 4
    }
    },
    # Youth Worship Night - March
    {
    "event_id": 1002,
    "event_type_id": 2,
    "fields": {
        "theme": "Light in the Darkness",
        "guest_band": "Awaken Youth",
        "is_livestreamed": True
    }
    },
    # Park Cleanup Day
    {
    "event_id": 1003,
    "event_type_id": 3,
    "fields": {
        "location": "Riverside Park",
        "requires_supplies": True,
        "hours_expected": 3
    }
    },
    # Lock-In Spring 2025
    {
    "event_id": 1004,
    "event_type_id": 4,
    "fields": {
        "games_planned": "dodgeball, karaoke, nerf tag",
        "lights_out_time": "1:30 AM",
        "snacks_provided": True
    }
    },
    # Honduras Mission Trip
    {
    "event_id": 1005,
    "event_type_id": 5,
    "fields": {
        "destination": "San Pedro Sula",
        "total_cost": 1400,
        "passport_required": True
    }
    },
    # Romans Bible Study Week 1
    {
    "event_id": 1006,
    "event_type_id": 6,
    "fields": {
        "topic": "Living Sacrifices",
        "chapter_range": "Romans 12:1-8",
        "has_discussion": True
    }
    },
    # Student Leader Bootcamp
    {
    "event_id": 1007,
    "event_type_id": 7,
    "fields": {
        "trainer_name": "Sarah Johnson",
        "num_modules": 6,
        "certificate_awarded": False
    }
    },
    # Bake Sale Fundraiser
    {
    "event_id": 1008,
    "event_type_id": 8,
    "fields": {
        "fundraising_goal": 500,
        "beneficiary": "Summer Camp Scholarships",
        "is_online": False
    }
    },
    # Saturday Camp Day
    {
    "event_id": 1009,
    "event_type_id": 9,
    "fields": {
        "activities": "archery, crafts, swimming",
        "waiver_required": True,
        "max_capacity": 120
    }
    },
    # Volunteer Orientation (April)
    {
    "event_id": 1010,
    "event_type_id": 10,
    "fields": {
        "orientation_leader": "Mark Davis",
        "expected_hours": 2,
        "background_check_required": True
    }
    }
]

# Only insert if collections are empty
try:
    if event_type_schemas.count_documents({}) == 0:
        event_type_schemas.insert_many(event_type_schemas_data)
        event_custom_fields.insert_many(event_custom_fields_data)
        print("MongoDB initialized with sample data")
    else:
        print("MongoDB data already exists, skipping initialization")
except Exception as e:
    print(f"MongoDB initialization note: {e}")

def get_mongo_connection():
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)