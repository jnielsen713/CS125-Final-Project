import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

# This will let us keep our user information private by reading it from an external file.
load_dotenv()

# Try-Except block to print an error message instead of crashing the program
# From Zybook
try:
    youthGroupConnection = mysql.connector.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', 3306),
        database=os.getenv('DB_NAME'))

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Invalid credentials')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database not found')
    else:
        print('Cannot connect to database:', err)

else:
    # The rest of the code will go here
    youthGroupConnection.close()
