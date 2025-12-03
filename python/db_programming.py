# For connection
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

# For API
from flask import Flask, jsonify, request

# Redis connection
from python.redis_connection import get_redis_connection
from datetime import datetime

r = get_redis_connection()

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

@app.get("/")
def read_root():
    # FILL THIS OUT
    pass

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
        ORDER BY p.lastName, p.firstName;
    """)
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
        ORDER BY p.lastName, p.firstName;
    """)
    rows = ygc.fetchall()
    ygc.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/upcoming-events")
def get_upcoming_events():
    youthGroupConnection = get_connection()
    ygc = youthGroupConnection.cursor()
    ygc.execute("SELECT * FROM Event WHERE startDateTime > NOW() ORDER BY startDateTime;")
    rows = ygc.fetchall()
    ygc.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/student/<int:student_id>/parents")
def get_student_parents(student_id):
    youthGroupConnection = get_connection()
    ygc = youthGroupConnection.cursor()
    ygc.execute("""SELECT p.personId, p.firstName, p.lastName, p.email, p.phone 
        FROM Person p 
        JOIN ParentChild pc ON p.personId = pc.parentId 
        WHERE pc.childId = %s
        ORDER BY p.lastName, p.firstName;
    """, (student_id,))
    rows = ygc.fetchall()
    ygc.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/parent/<int:parent_id>/children")
def get_parent(parent_id):
    youthGroupConnection = get_connection()
    ygc = youthGroupConnection.cursor()
    ygc.execute("""SELECT p.personId, p.firstName, p.lastName, p.birthday, p.email 
        FROM Person p 
        JOIN ParentChild pc ON p.personId = pc.childId 
        WHERE pc.parentId = %s
        ORDER BY p.birthday;
    """, (parent_id,))
    rows = ygc.fetchall()
    ygc.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/smallgroup/<int:group_id>/members")
def get_smallgroup_members(group_id):
    youthGroupConnection = get_connection()
    ygc = youthGroupConnection.cursor()
    ygc.execute("""SELECT p.personId, p.firstName, p.lastName, p.email, p.phone, sgm.joinedDate 
    FROM Person p 
    JOIN SmallGroupMembership sgm ON p.personId = sgm.studentId 
    WHERE sgm.smallGroupId = %s
    ORDER BY p.lastName, p.firstName;
    """, (group_id,))
    rows = ygc.fetchall()
    ygc.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/event/<int:event_id>/registrations")
def get_event_registrations(event_id):
    youthGroupConnection = get_connection()
    ygc = youthGroupConnection.cursor()
    ygc.execute("""SELECT p.personId, p.firstName, p.lastName, p.email, p.phone, er.registrationDate 
        FROM Person p 
        JOIN EventRegistration er ON p.personId = er.personId 
        WHERE er.eventId = %s
        ORDER BY er.registrationDate;
    """, (event_id,))
    rows = ygc.fetchall()
    ygc.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/event/<int:event_id>/attendances")
def get_event_attendances(event_id):
    youthGroupConnection = get_connection()
    ygc = youthGroupConnection.cursor()
    ygc.execute("""SELECT p.personId, p.firstName, p.lastName, a.checkedInAt, a.checkedOutAt 
        FROM Person p 
        JOIN Attendance a ON p.personId = a.personId 
        WHERE a.eventId = %s
        ORDER BY a.checkedInAt;
    """, (event_id,))
    rows = ygc.fetchall()
    ygc.close()
    youthGroupConnection.close()
    return jsonify(rows)

@app.get("/event/<int:event_id>/checkin/status")
def get_event_checkin_status(event_id):
    if not r:
        return jsonify({"error": "Redis connection not available"})
    checked_in_Ids = r.smembers(f"event:{event_id}:checkedIn")
    num_checked_in = r.scard(f"event:{event_id}:checkedIn")
    check_in_times = r.hgetall(f"event:{event_id}:checkInTimes")

    return jsonify({
        "event_id": event_id,
        "total_checked_in": num_checked_in,
        "student_Ids": sorted(list(checked_in_Ids)),
        "check_in_times": check_in_times,
    })

@app.post("/event/<int:event_id>/checkin/<int:student_id>")
def checkin_student(event_id, student_id):
    """Check in a student to an event in real-time using Redis"""
    if not r:
        return jsonify({"error": "Redis connection unavailable"}), 500

    try:
        # Add student to checked-in set
        r.sadd(f"event:{event_id}:checkedIn", student_id)

        # Record check-in time
        timestamp = datetime.now().isoformat()
        r.hset(f"event:{event_id}:checkInTimes", student_id, timestamp)

        # Get current count
        count = r.scard(f"event:{event_id}:checkedIn")

        return jsonify({
            "success": True,
            "student_id": student_id,
            "event_id": event_id,
            "checked_in_at": timestamp,
            "current_attendance": count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # fetch the primary key data from redis, then use that to run a sql query with the field specified
    # what you return should match the stuff specified in the pydantic models

if __name__ == "__main__":
    app.run(debug=True)

# Depending on the port, running http://127.0.0.1:5000/people in Insomnia should yield the proper results.
