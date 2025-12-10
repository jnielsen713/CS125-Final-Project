from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

uri = str(os.getenv('MONGO_URI'))

# Create a new client with SSL context workaround
try:
    # Create custom SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    client = MongoClient(
        uri,
        server_api=ServerApi('1'),
        tls=True,
        tlsAllowInvalidCertificates=True,
        tlsAllowInvalidHostnames=True,
        connect=False  # Don't connect immediately
    )
except Exception as e:
    print(f"MongoDB client creation error: {e}")
    raise

# Establish the database we are using
db = client["youth_group_database"]

# Populate with sample data for demo
event_type_schemas = db["event_type_schemas"]
event_custom_fields = db["event_custom_fields"]
event_notes_collection = db["event_notes"]

# Data provided by chatgpt
event_type_schemas_data = [
    # Retreat
    {
        "event_type_id": 1,
        "fields": [
            {"name": "packing_list", "type": "text"},
            {"name": "overnight", "type": "boolean"},
            {"name": "num_sessions", "type": "number"}
        ]
    },
    # Worship Night
    {
        "event_type_id": 2,
        "fields": [
            {"name": "theme", "type": "text"},
            {"name": "guest_band", "type": "text"},
            {"name": "is_livestreamed", "type": "boolean"}
        ]
    },
    # Service Project
    {
        "event_type_id": 3,
        "fields": [
            {"name": "location", "type": "text"},
            {"name": "requires_supplies", "type": "boolean"},
            {"name": "hours_expected", "type": "number"}
        ]
    },
    {
        "event_type_id": 4,
        "fields": [
            {"name": "games_planned", "type": "text"},
            {"name": "lights_out_time", "type": "text"},
            {"name": "snacks_provided", "type": "boolean"}
        ]
    },
    # Missions Trip
    {
        "event_type_id": 5,
        "fields": [
            {"name": "destination", "type": "text"},
            {"name": "total_cost", "type": "number"},
            {"name": "passport_required", "type": "boolean"}
        ]
    },
    # Bible Study
    {
        "event_type_id": 6,
        "fields": [
            {"name": "topic", "type": "text"},
            {"name": "chapter_range", "type": "text"},
            {"name": "has_discussion", "type": "boolean"}
        ]
    },
    # Leadership Training
    {
        "event_type_id": 7,
        "fields": [
            {"name": "trainer_name", "type": "text"},
            {"name": "num_modules", "type": "number"},
            {"name": "certificate_awarded", "type": "boolean"}
        ]
    },
    # Fundraiser
    {
        "event_type_id": 8,
        "fields": [
            {"name": "fundraising_goal", "type": "number"},
            {"name": "beneficiary", "type": "text"},
            {"name": "is_online", "type": "boolean"}
        ]
    },
    # Camp Day
    {
        "event_type_id": 9,
        "fields": [
            {"name": "activities", "type": "text"},
            {"name": "waiver_required", "type": "boolean"},
            {"name": "max_capacity", "type": "number"}
        ]
    },
    # Orientation Training
    {
        "event_type_id": 10,
        "fields": [
            {"name": "orientation_leader", "type": "text"},
            {"name": "expected_hours", "type": "number"},
            {"name": "background_check_required", "type": "boolean"}
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


event_notes_data = [
    # Winter Retreat 2025
    {
        "event_id": 1001,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Jessica Lee",
                "timestamp": "2025-01-12T14:30:00Z",
                "content": "Arrival went smoothly. A few students forgot items from the packing list, but leaders helped provide extras."
            },
            {
                "noteId": "a2f3c8de-9f0e-4b52-8e8c-2c3b94c9c412",
                "author": "David Kim",
                "timestamp": "2025-01-12T20:10:00Z",
                "content": "First session went great. Students were very engaged. One minor scrape during free time; handled by first aid team."
            }
        ]
    },

    # Youth Worship Night - March
    {
        "event_id": 1002,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Aaron Smith",
                "timestamp": "2025-03-08T19:55:00Z",
                "content": "Sound check was flawless. Guest band arrived early and were very easy to work with."
            },
            {
                "noteId": "4b8e2d7a-1c3f-4d21-ae65-9c0df45b8ab7",
                "author": "Maria Torres",
                "timestamp": "2025-03-08T21:20:00Z",
                "content": "Theme connected well—students responded strongly during prayer time."
            }
        ]
    },

    # Park Cleanup Day
    {
        "event_id": 1003,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Jake Martinez",
                "timestamp": "2025-04-05T10:45:00Z",
                "content": "Volunteers were enthusiastic. Supplies ran low halfway through; requested more trash bags."
            },
            {
                "noteId": "d71ac9f2-5c7a-4f28-9b13-2af0ee67bc10",
                "author": "Emily Carter",
                "timestamp": "2025-04-05T12:15:00Z",
                "content": "City rep thanked the group for participation. Total of 25 bags filled!"
            }
        ]
    },

    # Lock-In Spring 2025
    {
        "event_id": 1004,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Chris Nguyen",
                "timestamp": "2025-05-18T01:00:00Z",
                "content": "Games were a huge hit. Some students getting tired early; encouraged hydration and snack breaks."
            },
            {
                "noteId": "e0c44b3f-61ab-4f5f-8e74-8cf91ab8cdd3",
                "author": "Rachel Allen",
                "timestamp": "2025-05-18T02:40:00Z",
                "content": "Lights-out was later than planned, but students settled quickly. No behavioral issues."
            }
        ]
    },

    # Honduras Mission Trip
    {
        "event_id": 1005,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Mission Lead: Jonathan Perez",
                "timestamp": "2025-06-20T09:00:00Z",
                "content": "Travel day smooth. Customs took longer than expected, but all luggage arrived."
            },
            {
                "noteId": "7c9f5bd0-182e-47d4-8a38-2e8b7d6e2370",
                "author": "Assistant Leader: Lindsay Brooks",
                "timestamp": "2025-06-21T17:30:00Z",
                "content": "Worksite progress ahead of schedule. Students bonding well with local volunteers."
            }
        ]
    },

    # Romans Bible Study Week 1
    {
        "event_id": 1006,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Leader: Hannah Clark",
                "timestamp": "2025-09-03T18:15:00Z",
                "content": "Group discussion was surprisingly deep for week one. Students asked great questions."
            },
            {
                "noteId": "53dd3a80-8d51-43ce-a9a1-836eb17ecfa3",
                "author": "Leader: Sam Patel",
                "timestamp": "2025-09-03T19:40:00Z",
                "content": "Some students struggled with the text. Planning to send a follow-up summary email."
            }
        ]
    },

    # Student Leader Bootcamp
    {
        "event_id": 1007,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Trainer: Sarah Johnson",
                "timestamp": "2025-08-14T11:00:00Z",
                "content": "Module 1 complete. Students showed strong leadership potential and teamwork."
            },
            {
                "noteId": "2ef9d721-0a67-4d3a-917e-b109a6f8f312",
                "author": "Co-Trainer: Michael Chen",
                "timestamp": "2025-08-14T13:30:00Z",
                "content": "Afternoon session slower; may shorten content next year."
            }
        ]
    },

    # Bake Sale Fundraiser
    {
        "event_id": 1008,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Coordinator: Lisa Harper",
                "timestamp": "2025-10-10T09:50:00Z",
                "content": "Setup finished early. Students brought a great variety of baked goods."
            },
            {
                "noteId": "894d1e39-eb99-4125-8b37-fd5f53e67402",
                "author": "Finance Volunteer: Tom Gregory",
                "timestamp": "2025-10-10T14:30:00Z",
                "content": "Reached 80% of fundraising goal by midday. Very strong turnout from the community."
            }
        ]
    },

    # Saturday Camp Day
    {
        "event_id": 1009,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Camp Director: Valerie Stone",
                "timestamp": "2025-07-22T10:00:00Z",
                "content": "Archery station needed extra supervision due to high interest. No safety issues."
            },
            {
                "noteId": "af8d2773-6b19-47b0-937d-39c7dfc75c4d",
                "author": "Swimming Lead: Connor Williams",
                "timestamp": "2025-07-22T12:45:00Z",
                "content": "Swimming went great. Lifeguards reported excellent student behavior."
            }
        ]
    },

    # Volunteer Orientation (April)
    {
        "event_id": 1010,
        "notes": [
            {
                "noteId": "3db7ded1-0fbf-4178-89bc-6bbcf7abd431",
                "author": "Orientation Leader: Mark Davis",
                "timestamp": "2025-04-02T18:05:00Z",
                "content": "Group asked many good questions about safety protocols. Very engaged."
            },
            {
                "noteId": "c61d9fa1-4c8e-4a07-82df-12bcf9c77d25",
                "author": "Admin Support: Olivia White",
                "timestamp": "2025-04-02T19:00:00Z",
                "content": "All volunteers completed paperwork except one; will follow up tomorrow."
            }
        ]
    }
]




# Only insert if collections are empty
def initialize_data():
    try:
        changed = False
        if event_type_schemas.count_documents({}) == 0:
            event_type_schemas.insert_many(event_type_schemas_data)
            changed = True
        if event_custom_fields.count_documents({}) == 0:
            event_custom_fields.insert_many(event_custom_fields_data)
            changed = True
        if event_notes_collection.count_documents({}) == 0:
            event_notes_collection.insert_many(event_notes_data)
            changed = True
        if changed:
            print("✓ MongoDB initialized with sample data.")
        else:
            print("ℹ MongoDB already contains data; initialization skipped.")
    except Exception as e:
        print(f"⚠ MongoDB initialization warning: {e}")


def get_mongo_connection():
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("✓ Pinged your deployment. You successfully connected to MongoDB!")
        initialize_data()
        return client
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        raise  # Re-raise to stop the application