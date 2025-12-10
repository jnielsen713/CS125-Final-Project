# For connection
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

# For API
from flask import Flask, jsonify, request

# Redis connection
from mongo_connection import get_mongo_connection, event_type_schemas, event_custom_fields
from redis_connection import get_redis_connection
from datetime import datetime

from strawberry.flask.views import GraphQLView
from graphql_schema import schema
from mysql_connection import get_connection

m = get_mongo_connection()
r = get_redis_connection()

# This will let us keep our user information private by reading it from an external file.
load_dotenv()

# API
app = Flask(__name__)

# Test endpoint
@app.get("/ping")
def ping():
    return "pong"

# MYSQL ENDPOINTS ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    # FILL THIS OUT
    return "root"


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

@app.get("/event-types")
def get_event_types():
    youthGroupConnection = get_connection()
    youthGroupCursor = youthGroupConnection.cursor()
    youthGroupCursor.execute("SELECT eventTypeId, name FROM EventType;")
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


# ============================================================================
# SMALL GROUP MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/smallgroup/<int:group_id>/add-student/<int:student_id>")
def add_student_to_smallgroup(group_id, student_id):
    """Add a student to a small group"""
    try:
        youthGroupConnection = get_connection()
        ygc = youthGroupConnection.cursor()

        # Check if a student exists and is a student
        ygc.execute("""
                    SELECT p.personId, p.firstName, p.lastName
                    FROM Person p
                             JOIN PersonRole pr ON p.personId = pr.personId
                    WHERE p.personId = %s
                      AND pr.roleId = 1;
                    """, (student_id,))

        student = ygc.fetchone()
        if not student:
            ygc.close()
            youthGroupConnection.close()
            return jsonify({"error": "Student not found"}), 404

        # Check if a small group exists
        ygc.execute("SELECT smallGroupId, name FROM SmallGroup WHERE smallGroupId = %s;", (group_id,))
        group = ygc.fetchone()
        if not group:
            ygc.close()
            youthGroupConnection.close()
            return jsonify({"error": "Small group not found"}), 404

        # Add student to a small group
        joined_date = datetime.now().date()
        ygc.execute("""
                    INSERT INTO SmallGroupMembership (studentId, smallGroupId, joinedDate)
                    VALUES (%s, %s, %s);
                    """, (student_id, group_id, joined_date))

        youthGroupConnection.commit()
        ygc.close()
        youthGroupConnection.close()

        return jsonify({
            "success": True,
            "message": f"{student[1]} {student[2]} added to {group[1]}",
            "student_id": student_id,
            "group_id": group_id,
            "joined_date": joined_date.isoformat()
        })

    except mysql.connector.IntegrityError:
        return jsonify({"error": "Student is already in this small group"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.delete("/smallgroup/<int:group_id>/remove-student/<int:student_id>")
def remove_student_from_smallgroup(group_id, student_id):
    """Remove a student from a small group"""
    try:
        youthGroupConnection = get_connection()
        ygc = youthGroupConnection.cursor()

        # Remove student from small group
        ygc.execute("""
                    DELETE
                    FROM SmallGroupMembership
                    WHERE studentId = %s
                      AND smallGroupId = %s;
                    """, (student_id, group_id))

        if ygc.rowcount == 0:
            ygc.close()
            youthGroupConnection.close()
            return jsonify({"error": "Student was not in this small group"}), 404

        youthGroupConnection.commit()
        ygc.close()
        youthGroupConnection.close()

        return jsonify({
            "success": True,
            "message": "Student removed from small group",
            "student_id": student_id,
            "group_id": group_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# EVENT REGISTRATION ENDPOINTS
# ============================================================================

@app.post("/event/<int:event_id>/register/<int:person_id>")
def register_for_event(event_id, person_id):
    """Register a person for an event"""
    try:
        youthGroupConnection = get_connection()
        ygc = youthGroupConnection.cursor()

        # Check if person exists
        ygc.execute("SELECT personId, firstName, lastName FROM Person WHERE personId = %s;", (person_id,))
        person = ygc.fetchone()
        if not person:
            ygc.close()
            youthGroupConnection.close()
            return jsonify({"error": "Person not found"}), 404

        # Check if event exists
        ygc.execute("SELECT eventId, eventName FROM Event WHERE eventId = %s;", (event_id,))
        event = ygc.fetchone()
        if not event:
            ygc.close()
            youthGroupConnection.close()
            return jsonify({"error": "Event not found"}), 404

        # Register person for event
        registration_date = datetime.now()
        ygc.execute("""
                    INSERT INTO EventRegistration (personId, eventId, registrationDate)
                    VALUES (%s, %s, %s);
                    """, (person_id, event_id, registration_date))

        youthGroupConnection.commit()
        ygc.close()
        youthGroupConnection.close()

        return jsonify({
            "success": True,
            "message": f"{person[1]} {person[2]} registered for {event[1]}",
            "person_id": person_id,
            "event_id": event_id,
            "registration_date": registration_date.isoformat()
        })

    except mysql.connector.IntegrityError:
        return jsonify({"error": "Person is already registered for this event"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.delete("/event/<int:event_id>/unregister/<int:person_id>")
def unregister_from_event(event_id, person_id):
    """Unregister a person from an event"""
    try:
        youthGroupConnection = get_connection()
        ygc = youthGroupConnection.cursor()

        # Remove registration
        ygc.execute("""
                    DELETE
                    FROM EventRegistration
                    WHERE personId = %s
                      AND eventId = %s;
                    """, (person_id, event_id))

        if ygc.rowcount == 0:
            ygc.close()
            youthGroupConnection.close()
            return jsonify({"error": "Person was not registered for this event"}), 404

        youthGroupConnection.commit()
        ygc.close()
        youthGroupConnection.close()

        return jsonify({
            "success": True,
            "message": "Registration removed",
            "person_id": person_id,
            "event_id": event_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/person/<int:person_id>/registrations")
def get_person_registrations(person_id):
    """Get all events a person is registered for"""
    try:
        youthGroupConnection = get_connection()
        ygc = youthGroupConnection.cursor()

        ygc.execute("""
                    SELECT e.eventId, e.eventName, e.startDateTime, e.location, er.registrationDate
                    FROM Event e
                             JOIN EventRegistration er ON e.eventId = er.eventId
                    WHERE er.personId = %s
                    ORDER BY e.startDateTime;
                    """, (person_id,))

        rows = ygc.fetchall()
        ygc.close()
        youthGroupConnection.close()

        return jsonify(rows)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# REDIS ENDPOINTS ---------------------------------------------------------------------------

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


@app.post("/event/<int:event_id>/checkout/<int:student_id>")
def checkout_student(event_id, student_id):
    """Check out a student from an event using Redis"""
    if not r:
        return jsonify({"error": "Redis connection unavailable"}), 500

    try:
        # Remove student from a checked-in set
        removed = r.srem(f"event:{event_id}:checkedIn", student_id)

        if not removed:
            return jsonify({"error": "Student was not checked in"}), 404

        # Record check-out time
        timestamp = datetime.now().isoformat()
        r.hset(f"event:{event_id}:checkOutTimes", student_id, timestamp)

        # Get current count
        count = r.scard(f"event:{event_id}:checkedIn")

        return jsonify({
            "success": True,
            "student_id": student_id,
            "event_id": event_id,
            "checked_out_at": timestamp,
            "current_attendance": count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/event/<int:event_id>/finalize")
def finalize_event_attendance(event_id):
    """
    Finalize event - persist Redis check-in data to MySQL Attendance table
    and clear Redis keys
    """
    if not r:
        return jsonify({"error": "Redis connection unavailable"}), 500

    try:
        # Get all checked-in students and their times
        checked_in_ids = r.smembers(f"event:{event_id}:checkedIn")
        check_in_times = r.hgetall(f"event:{event_id}:checkInTimes")
        check_out_times = r.hgetall(f"event:{event_id}:checkOutTimes")

        if not checked_in_ids:
            return jsonify({
                "success": True,
                "message": "No attendance to finalize",
                "records_saved": 0
            })

        youthGroupConnection = get_connection()
        ygc = youthGroupConnection.cursor()

        records_saved = 0

        for student_id in checked_in_ids:
            student_id_str = str(student_id)
            check_in_time = check_in_times.get(student_id_str)
            check_out_time = check_out_times.get(student_id_str, None)

            if check_in_time:
                # Insert into Attendance table
                ygc.execute("""
                            INSERT INTO Attendance (personId, eventId, checkedInAt, checkedOutAt)
                            VALUES (%s, %s, %s, %s) ON DUPLICATE KEY
                            UPDATE
                                checkedInAt =
                            VALUES (checkedInAt), checkedOutAt =
                            VALUES (checkedOutAt);
                            """, (int(student_id), event_id, check_in_time, check_out_time))
                records_saved += 1

        youthGroupConnection.commit()
        ygc.close()
        youthGroupConnection.close()

        # Clear Redis keys
        r.delete(
            f"event:{event_id}:checkedIn",
            f"event:{event_id}:checkInTimes",
            f"event:{event_id}:checkOutTimes"
        )

        return jsonify({
            "success": True,
            "message": "Attendance finalized and persisted to MySQL",
            "records_saved": records_saved
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/events/active")
def get_all_active_events():
    """
    Get all events that currently have people checked in (live events).
    Useful for administrative dashboard to see what's happening RIGHT NOW.
    """
    if not r:
        return jsonify({"error": "Redis connection unavailable"}), 500

    try:
        # Scan for all event check-in keys in Redis
        active_events = []

        # Get all keys matching the pattern
        for key in r.scan_iter(match="event:*:checkedIn"):
            # Extract event ID from key (format: "event:123:checkedIn")
            event_id = int(key.split(':')[1])
            count = r.scard(key)

            if count > 0:  # Only include events with people checked in
                # Get event details from MySQL
                youthGroupConnection = get_connection()
                ygc = youthGroupConnection.cursor()
                ygc.execute("""
                            SELECT eventId, eventName, startDateTime, location
                            FROM Event
                            WHERE eventId = %s;
                            """, (event_id,))
                event = ygc.fetchone()
                ygc.close()
                youthGroupConnection.close()

                if event:
                    active_events.append({
                        "event_id": event_id,
                        "event_name": event[1],
                        "start_time": event[2].isoformat() if event[2] else None,
                        "location": event[3],
                        "current_attendance": count
                    })

        return jsonify({
            "active_events": active_events,
            "total_active_events": len(active_events),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/dashboard/live")
def get_live_dashboard():
    """
    Comprehensive live dashboard - shows all active events and their attendance.
    This is what an administrator would see on their main screen.
    """
    if not r:
        return jsonify({"error": "Redis connection unavailable"}), 500

    try:
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "active_events": [],
            "total_people_across_all_events": 0
        }

        # Get all active event check-in keys
        for key in r.scan_iter(match="event:*:checkedIn"):
            event_id = int(key.split(':')[1])
            count = r.scard(key)

            if count > 0:
                # Get event details from MySQL
                youthGroupConnection = get_connection()
                ygc = youthGroupConnection.cursor()
                ygc.execute("""
                            SELECT e.eventId, e.eventName, e.startDateTime, e.location, e.eventTypeId
                            FROM Event e
                            WHERE e.eventId = %s;
                            """, (event_id,))
                event = ygc.fetchone()

                if event:
                    # Get checked-in student IDs
                    checked_in_ids = list(r.smembers(key))

                    # Get student names
                    if checked_in_ids:
                        placeholders = ','.join(['%s'] * len(checked_in_ids))
                        query = f"""
                            SELECT p.personId, p.firstName, p.lastName
                            FROM Person p
                            WHERE p.personId IN ({placeholders})
                            ORDER BY p.lastName, p.firstName;
                        """
                        ygc.execute(query, [int(id) for id in checked_in_ids])
                        students = ygc.fetchall()

                        student_list = [{
                            "id": s[0],
                            "name": f"{s[1]} {s[2]}"
                        } for s in students]
                    else:
                        student_list = []

                    ygc.close()
                    youthGroupConnection.close()

                    dashboard_data["active_events"].append({
                        "event_id": event_id,
                        "event_name": event[1],
                        "event_type": event[4],
                        "start_time": event[2].isoformat() if event[2] else None,
                        "location": event[3],
                        "current_attendance": count,
                        "students": student_list
                    })

                    dashboard_data["total_people_across_all_events"] += count

        dashboard_data["number_of_active_events"] = len(dashboard_data["active_events"])

        return jsonify(dashboard_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# MONGO ENDPOINTS ---------------------------------------------------------------------------

# Get all event type schemas
@app.get("/event-type-schemas")
def get_all_event_type_schemas():
    # Fetch all documents, hide internal ObjectId
    docs = list(event_type_schemas.find({}, {"_id": 0}))
    return jsonify({"event_types": docs})


# Get all individual events
@app.get("/events/custom-data")
def get_all_event_custom_data():
    # Fetch all custom event data documents from MongoDB
    docs = list(event_custom_fields.find({}, {"_id": 0}))
    return jsonify({"event_custom_data": docs})


# Insert or update a single event at the specified event_id
# Insert or update a single event at the specified event_id
@app.post("/event/custom-data")
def create_or_update_event():
    data = request.get_json()

    # --- Validate base JSON ---
    required_sql_fields = ["event_type_id", "event_name", "startDateTime", "location"]
    missing = [f for f in required_sql_fields if f not in data]

    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    if "custom_data" not in data:
        return jsonify({"error": "custom_data is required"}), 400

    event_type_id = data["event_type_id"]
    event_name = data["event_name"]
    start_dt = data["startDateTime"]
    location = data["location"]
    custom_data = data["custom_data"]

    youthGroupConnection = None
    ygc = None

    try:
        youthGroupConnection = get_connection()
        if youthGroupConnection is None:
            return jsonify({"error": "Could not connect to MySQL"}), 500

        ygc = youthGroupConnection.cursor()

        # --- Check for existing event by name and start time (your unique constraints may vary) ---
        ygc.execute("""
            SELECT eventId FROM Event
            WHERE eventName = %s AND startDateTime = %s
        """, (event_name, start_dt))

        existing = ygc.fetchone()

        if existing:
            # ------------------------------------
            # UPDATE EXISTING EVENT
            # ------------------------------------
            event_id = existing[0]

            ygc.execute("""
                UPDATE Event
                SET eventTypeId = %s, location = %s
                WHERE eventId = %s
            """, (event_type_id, location, event_id))

            youthGroupConnection.commit()

        else:
            # ------------------------------------
            # CREATE NEW EVENT
            # ------------------------------------
            ygc.execute("""
                INSERT INTO Event (eventName, eventTypeId, startDateTime, location)
                VALUES (%s, %s, %s, %s)
            """, (event_name, event_type_id, start_dt, location))

            youthGroupConnection.commit()

            event_id = ygc.lastrowid  # MySQL auto-increment ID

    except Exception as e:
        return jsonify({"error": f"MySQL operation failed: {str(e)}"}), 500

    finally:
        if ygc:
            ygc.close()
        if youthGroupConnection:
            youthGroupConnection.close()

    # ------------------------------------
    # MONGODB UPSERT (no duplicates)
    # ------------------------------------
    try:
        event_custom_fields.replace_one(
            {"eventId": event_id},   # filter
            {
                "eventId": event_id,
                "eventTypeId": event_type_id,
                "custom_data": custom_data
            },
            upsert=True
        )

    except Exception as e:
        return jsonify({"error": f"MongoDB operation failed: {str(e)}"}), 500

    return jsonify({
        "message": "Event saved (created or updated)",
        "eventId": event_id,
        "event_type_id": event_type_id,
        "event_name": event_name,
        "startDateTime": start_dt,
        "location": location,
        "custom_data": custom_data
    }), 201


@app.post("/event-type")
def create_or_update_event_type():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    if "name" not in data:
        return jsonify({"error": "name is required"}), 400

    if "fields" not in data or not isinstance(data["fields"], list):
        return jsonify({"error": "fields must be a list"}), 400

    name = data["name"]
    fields = data["fields"]

    youthGroupConnection = None
    ygc = None
    event_type_id = None

    try:
        youthGroupConnection = get_connection()
        if youthGroupConnection is None:
            return jsonify({"error": "Could not connect to MySQL"}), 500
        ygc = youthGroupConnection.cursor()

        # Does an event type with this name already exist?
        ygc.execute("SELECT eventTypeId FROM EventType WHERE name = %s", (name,))
        row = ygc.fetchone()

        if not row:
            # Create a new event type
            ygc.execute("INSERT INTO EventType (name) VALUES (%s)", (name,))
            youthGroupConnection.commit()

            event_type_id = ygc.lastrowid

        else:
            # Overwrite existing event type
            event_type_id = row[0]

            # OPTIONAL: Update name field if your system allows renaming
            # ygc.execute("UPDATE EventType SET name = %s WHERE eventTypeId = %s",
            #             (name, event_type_id))

            youthGroupConnection.commit()

    except Exception as e:
        return jsonify({"error": f"MySQL operation failed: {str(e)}"}), 500

    finally:
        if ygc:
            ygc.close()
        if youthGroupConnection:
            youthGroupConnection.close()

    # --- MongoDB: Upsert the schema for this event type ---
    try:
        event_type_schemas.update_one(
            {"event_type_id": event_type_id},   # find existing
            {"$set": {
                "event_type_id": event_type_id,
                "fields": fields
            }},
            upsert=True
        )

    except Exception as e:
        return jsonify({"error": f"MongoDB operation failed: {str(e)}"}), 500


    return jsonify({
        "message": "Event type saved (new or overwritten)",
        "event_type_id": event_type_id,
        "name": name,
        "fields": fields
    }), 201

# ============================================================================
# GRAPHQL ENDPOINT
# ============================================================================

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
)

# The graphiql=True parameter enables GraphiQL - an interactive GraphQL playground
# Access it at: http://localhost:5000/graphql

# Run app -----------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

# Depending on the port, running http://127.0.0.1:5000/people in Insomnia should yield the proper results.
