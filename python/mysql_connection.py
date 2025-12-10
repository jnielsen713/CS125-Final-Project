"""
MySQL connection module for Youth Group Database
Extracted to avoid circular imports with GraphQL schema
"""

import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def get_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Returns None if connection fails.
    """
    youth_group_connection = None
    try:
        youth_group_connection = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 3306),
            database=os.getenv('DB_NAME')
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Invalid credentials')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database not found')
        else:
            print('Cannot connect to database:', err)

    return youth_group_connection