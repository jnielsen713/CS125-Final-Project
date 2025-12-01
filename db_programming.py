# For connection
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

# For API
from flask import Flask, jsonify, request

# This will let us keep our user information private by reading it from an external file.
load_dotenv()

# Try-Except block to print an error message instead of crashing the program
# From Zybook
def get_connection():
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
    
    return youthGroupConnection

# API
app = Flask(__name__)

@app.get("/people")
def get_people():
    youthGroupConnection = get_connection()
    youthGroupCursor = youthGroupConnection.cursor()
    youthGroupCursor.execute("SELECT firstName, lastName, email, phone FROM Person;")
    rows = youthGroupCursor.fetchall()
    youthGroupCursor.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/events")
def get_events():
    youthGroupConnection = get_connection()
    youthGroupCursor = youthGroupConnection.cursor()
    youthGroupCursor.execute("SELECT eventName, startDateTime, location FROM Event;")
    rows = youthGroupCursor.fetchall()
    youthGroupCursor.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/smallgroups")
def get_smallgroups():
    youthGroupConnection = get_connection()
    youthGroupCursor = youthGroupConnection.cursor()
    youthGroupCursor.execute("SELECT name, description FROM SmallGroup;")
    rows = youthGroupCursor.fetchall()
    youthGroupCursor.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/students")
def get_students():
    youthGroupConnection = get_connection()
    youthGroupCursor = youthGroupConnection.cursor()
    youthGroupCursor.execute("""SELECT p.personId, p.firstName, p.lastName, p.email, p.phone, p.birthday 
        FROM Person p 
        JOIN PersonRole pr ON p.personId = pr.personId 
        WHERE pr.roleId = 1
        ORDER BY p.lastName, p.firstName;""")
    rows = youthGroupCursor.fetchall()
    youthGroupCursor.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/parents")
def get_parents():
    youthGroupConnection = get_connection()
    ygc = youthGroupConnection.cursor()
    ygc.execute("""SELECT p.personId, p.firstName, p.lastName, p.email, p.phone 
        FROM Person p 
        JOIN PersonRole pr ON p.personId = pr.personId 
        WHERE pr.roleId = 2
        ORDER BY p.lastName, p.firstName;""")
    rows = ygc.fetchall()
    ygc.close()
    youthGroupConnection.close()
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)

# Depending on the port, running http://127.0.0.1:5000/people in Insomnia should yield the proper results.
