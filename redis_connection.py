""" Westmont College CS 125 Database Design Fall 2025
    Final Project Youth Group Database Redis Connection
    Assistant Professor Mike Ryu
    Tim Klug and Joshua Nielsen
"""

import redis
import os
from dotenv import load_dotenv

load_dotenv()

def get_redis_connection():
    try:
        r = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True
        )
        r.ping()
        return r
    except redis.ConnectionError as e:
        print("Redis Connection Error: {}".format(e))
        return None