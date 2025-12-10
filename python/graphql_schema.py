"""
Youth Group Management System - GraphQL Schema

This GraphQL layer provides a unified API over three databases:
- MySQL: Core relational data (people, events, groups)
- MongoDB: Flexible document data (event custom fields, notes)
- Redis: Live state (real-time check-ins)

The schema demonstrates:
1. Type definitions matching our domain models
2. Resolvers that coordinate across multiple databases
3. Queries for reading data
4. Mutations for write operations
"""

import strawberry
from typing import List, Optional
from datetime import datetime
import json

# Import database connections
from mysql_connection import get_connection
from mongo_connection import get_mongo_connection, event_type_schemas, event_custom_fields
from redis_connection import get_redis_connection

# Get database clients
m = get_mongo_connection()
r = get_redis_connection()


# ============================================================================
# GRAPHQL TYPE DEFINITIONS
# ============================================================================

@strawberry.type
class Person:
    """Represents a person in the youth group (student, parent, leader, volunteer)"""
    person_id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[str] = None  # Will be formatted as ISO string


@strawberry.type
class Role:
    """Role type (Student, Parent, Leader, Volunteer)"""
    role_id: int
    name: str


@strawberry.type
class PersonWithRoles:
    """Person with their assigned roles"""
    person_id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[str] = None
    roles: List[Role]


@strawberry.type
class EventType:
    """Type of event (Retreat, Worship Night, Service Project, etc.)"""
    event_type_id: int
    name: str


@strawberry.type
class Event:
    """An event in the youth group schedule"""
    event_id: int
    event_name: str
    event_type_id: int
    event_type_name: Optional[str] = None
    start_date_time: str
    end_date_time: Optional[str] = None
    location: str


@strawberry.type
class EventRegistration:
    """A person's registration for an event"""
    person: Person
    event: Event
    registration_date: str


@strawberry.type
class SmallGroup:
    """A small group in the youth ministry"""
    small_group_id: int
    name: str
    description: Optional[str] = None
    leader: Optional[Person] = None


@strawberry.type
class SmallGroupMembership:
    """Student membership in a small group"""
    student: Person
    small_group: SmallGroup
    joined_date: str


@strawberry.type
class EventCustomData:
    """Flexible custom data for events stored in MongoDB"""
    event_id: int
    event_type_id: int
    custom_data: strawberry.scalars.JSON


@strawberry.type
class EventWithCustomData:
    """Event combined with its custom MongoDB data"""
    event_id: int
    event_name: str
    event_type_id: int
    start_date_time: str
    location: str
    custom_data: Optional[strawberry.scalars.JSON] = None


@strawberry.type
class LiveEventStatus:
    """Real-time check-in status from Redis"""
    event_id: int
    total_checked_in: int
    checked_in_students: List[Person]
    check_in_times: strawberry.scalars.JSON


@strawberry.type
class ActiveEvent:
    """An event that currently has people checked in"""
    event_id: int
    event_name: str
    start_time: Optional[str] = None
    location: str
    current_attendance: int


@strawberry.type
class Attendance:
    """Attendance record for an event"""
    person: Person
    event: Event
    checked_in_at: str
    checked_out_at: Optional[str] = None


# ============================================================================
# INPUT TYPES FOR MUTATIONS
# ============================================================================

@strawberry.input
class EventCustomDataInput:
    """Input for adding/updating custom event data"""
    event_name: Optional[str] = None
    event_type_id: Optional[int] = None
    start_date_time: Optional[str] = None
    location: Optional[str] = None
    custom_data: strawberry.scalars.JSON


@strawberry.input
class CheckInInput:
    """Input for checking in a student"""
    student_id: int
    event_id: int


# ============================================================================
# QUERY RESOLVERS
# ============================================================================

def get_all_people_resolver() -> List[Person]:
    """Fetch all people from MySQL"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("""
                       SELECT personId, firstName, lastName, email, phone, birthday
                       FROM Person
                       ORDER BY lastName, firstName
                       """)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        return [
            Person(
                person_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                phone=row[4],
                birthday=row[5].isoformat() if row[5] else None
            )
            for row in rows
        ]
    except Exception as e:
        raise Exception(f"Error fetching people: {e}")


def get_person_by_id_resolver(person_id: int) -> Optional[Person]:
    """Fetch a single person by ID"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("""
                       SELECT personId, firstName, lastName, email, phone, birthday
                       FROM Person
                       WHERE personId = %s
                       """, (person_id,))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()

        if not row:
            return None

        return Person(
            person_id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            phone=row[4],
            birthday=row[5].isoformat() if row[5] else None
        )
    except Exception as e:
        raise Exception(f"Error fetching person: {e}")


def get_all_students_resolver() -> List[Person]:
    """Fetch all students (roleId = 1)"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("""
                       SELECT p.personId, p.firstName, p.lastName, p.email, p.phone, p.birthday
                       FROM Person p
                                JOIN PersonRole pr ON p.personId = pr.personId
                       WHERE pr.roleId = 1
                       ORDER BY p.lastName, p.firstName
                       """)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        return [
            Person(
                person_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                phone=row[4],
                birthday=row[5].isoformat() if row[5] else None
            )
            for row in rows
        ]
    except Exception as e:
        raise Exception(f"Error fetching students: {e}")


def get_all_events_resolver() -> List[Event]:
    """Fetch all events with their type names"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("""
                       SELECT e.eventId,
                              e.eventName,
                              e.eventTypeId,
                              et.name,
                              e.startDateTime,
                              e.endDateTime,
                              e.location
                       FROM Event e
                                JOIN EventType et ON e.eventTypeId = et.eventTypeId
                       ORDER BY e.startDateTime DESC
                       """)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        return [
            Event(
                event_id=row[0],
                event_name=row[1],
                event_type_id=row[2],
                event_type_name=row[3],
                start_date_time=row[4].isoformat() if row[4] else "",
                end_date_time=row[5].isoformat() if row[5] else None,
                location=row[6]
            )
            for row in rows
        ]
    except Exception as e:
        raise Exception(f"Error fetching events: {e}")


def get_event_by_id_resolver(event_id: int) -> Optional[Event]:
    """Fetch a single event by ID"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("""
                       SELECT e.eventId,
                              e.eventName,
                              e.eventTypeId,
                              et.name,
                              e.startDateTime,
                              e.endDateTime,
                              e.location
                       FROM Event e
                                JOIN EventType et ON e.eventTypeId = et.eventTypeId
                       WHERE e.eventId = %s
                       """, (event_id,))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()

        if not row:
            return None

        return Event(
            event_id=row[0],
            event_name=row[1],
            event_type_id=row[2],
            event_type_name=row[3],
            start_date_time=row[4].isoformat() if row[4] else "",
            end_date_time=row[5].isoformat() if row[5] else None,
            location=row[6]
        )
    except Exception as e:
        raise Exception(f"Error fetching event: {e}")


def get_event_registrations_resolver(event_id: int) -> List[Person]:
    """Get all people registered for an event"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("""
                       SELECT p.personId, p.firstName, p.lastName, p.email, p.phone, p.birthday
                       FROM Person p
                                JOIN EventRegistration er ON p.personId = er.personId
                       WHERE er.eventId = %s
                       ORDER BY er.registrationDate
                       """, (event_id,))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        return [
            Person(
                person_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                phone=row[4],
                birthday=row[5].isoformat() if row[5] else None
            )
            for row in rows
        ]
    except Exception as e:
        raise Exception(f"Error fetching registrations: {e}")


def get_all_small_groups_resolver() -> List[SmallGroup]:
    """Fetch all small groups"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("""
                       SELECT sg.smallGroupId,
                              sg.name,
                              sg.description,
                              sg.leaderId,
                              p.firstName,
                              p.lastName
                       FROM SmallGroup sg
                                LEFT JOIN Person p ON sg.leaderId = p.personId
                       ORDER BY sg.name
                       """)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        groups = []
        for row in rows:
            leader = None
            if row[3]:  # if leaderId exists
                leader = Person(
                    person_id=row[3],
                    first_name=row[4],
                    last_name=row[5],
                    email=None,
                    phone=None,
                    birthday=None
                )

            groups.append(SmallGroup(
                small_group_id=row[0],
                name=row[1],
                description=row[2],
                leader=leader
            ))

        return groups
    except Exception as e:
        raise Exception(f"Error fetching small groups: {e}")


def get_small_group_members_resolver(group_id: int) -> List[Person]:
    """Get all members of a small group"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("""
                       SELECT p.personId, p.firstName, p.lastName, p.email, p.phone, p.birthday
                       FROM Person p
                                JOIN SmallGroupMembership sgm ON p.personId = sgm.studentId
                       WHERE sgm.smallGroupId = %s
                       ORDER BY p.lastName, p.firstName
                       """, (group_id,))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        return [
            Person(
                person_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                phone=row[4],
                birthday=row[5].isoformat() if row[5] else None
            )
            for row in rows
        ]
    except Exception as e:
        raise Exception(f"Error fetching group members: {e}")


# ============================================================================
# MONGODB RESOLVERS
# ============================================================================

def get_event_custom_data_resolver(event_id: int) -> Optional[EventCustomData]:
    """Fetch custom data for an event from MongoDB"""
    try:
        doc = event_custom_fields.find_one({"eventId": event_id}, {"_id": 0})

        if not doc:
            return None

        return EventCustomData(
            event_id=doc["eventId"],
            event_type_id=doc["eventTypeId"],
            custom_data=doc.get("custom_data", {})
        )
    except Exception as e:
        raise Exception(f"Error fetching custom data: {e}")


def get_event_with_custom_data_resolver(event_id: int) -> Optional[EventWithCustomData]:
    """Fetch event from MySQL and combine with MongoDB custom data"""
    try:
        # Get event from MySQL
        event = get_event_by_id_resolver(event_id)
        if not event:
            return None

        # Get custom data from MongoDB
        mongo_doc = event_custom_fields.find_one({"eventId": event_id}, {"_id": 0})
        custom_data = mongo_doc.get("custom_data") if mongo_doc else None

        return EventWithCustomData(
            event_id=event.event_id,
            event_name=event.event_name,
            event_type_id=event.event_type_id,
            start_date_time=event.start_date_time,
            location=event.location,
            custom_data=custom_data
        )
    except Exception as e:
        raise Exception(f"Error fetching event with custom data: {e}")


# ============================================================================
# REDIS RESOLVERS (LIVE DATA)
# ============================================================================

def get_live_event_status_resolver(event_id: int) -> LiveEventStatus:
    """Get real-time check-in status from Redis"""
    if not r:
        raise Exception("Redis connection not available")

    try:
        # Get checked-in student IDs from Redis
        checked_in_ids = r.smembers(f"event:{event_id}:checkedIn")
        check_in_times = r.hgetall(f"event:{event_id}:checkInTimes")

        # Hydrate with full Person data from MySQL
        students = []
        if checked_in_ids:
            cnx = get_connection()
            cursor = cnx.cursor()

            # Convert Redis set to list of integers
            id_list = [int(id) for id in checked_in_ids]
            placeholders = ','.join(['%s'] * len(id_list))

            query = f"""
                SELECT personId, firstName, lastName, email, phone, birthday
                FROM Person
                WHERE personId IN ({placeholders})
                ORDER BY lastName, firstName
            """
            cursor.execute(query, id_list)
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()

            students = [
                Person(
                    person_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    phone=row[4],
                    birthday=row[5].isoformat() if row[5] else None
                )
                for row in rows
            ]

        return LiveEventStatus(
            event_id=event_id,
            total_checked_in=len(checked_in_ids),
            checked_in_students=students,
            check_in_times=check_in_times
        )
    except Exception as e:
        raise Exception(f"Error fetching live status: {e}")


def get_active_events_resolver() -> List[ActiveEvent]:
    """Get all events with active check-ins from Redis"""
    if not r:
        raise Exception("Redis connection not available")

    try:
        active_events = []

        # Scan for all event check-in keys
        for key in r.scan_iter(match="event:*:checkedIn"):
            event_id = int(key.split(':')[1])
            count = r.scard(key)

            if count > 0:
                # Get event details from MySQL
                event = get_event_by_id_resolver(event_id)
                if event:
                    active_events.append(ActiveEvent(
                        event_id=event_id,
                        event_name=event.event_name,
                        start_time=event.start_date_time,
                        location=event.location,
                        current_attendance=count
                    ))

        return active_events
    except Exception as e:
        raise Exception(f"Error fetching active events: {e}")


# ============================================================================
# MUTATION RESOLVERS
# ============================================================================

def register_for_event_resolver(person_id: int, event_id: int) -> bool:
    """Register a person for an event"""
    try:
        cnx = get_connection()
        cursor = cnx.cursor()

        cursor.execute("""
                       INSERT INTO EventRegistration (personId, eventId, registrationDate)
                       VALUES (%s, %s, NOW())
                       """, (person_id, event_id))

        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except Exception as e:
        raise Exception(f"Error registering for event: {e}")


def check_in_student_resolver(student_id: int, event_id: int) -> LiveEventStatus:
    """Check in a student to an event (writes to Redis)"""
    if not r:
        raise Exception("Redis connection not available")

    try:
        # Add to Redis set
        r.sadd(f"event:{event_id}:checkedIn", student_id)

        # Record timestamp
        timestamp = datetime.now().isoformat()
        r.hset(f"event:{event_id}:checkInTimes", student_id, timestamp)

        # Return updated status
        return get_live_event_status_resolver(event_id)
    except Exception as e:
        raise Exception(f"Error checking in student: {e}")


def check_out_student_resolver(student_id: int, event_id: int) -> LiveEventStatus:
    """Check out a student from an event (updates Redis)"""
    if not r:
        raise Exception("Redis connection not available")

    try:
        # Remove from checked-in set
        r.srem(f"event:{event_id}:checkedIn", student_id)

        # Record checkout time
        timestamp = datetime.now().isoformat()
        r.hset(f"event:{event_id}:checkOutTimes", student_id, timestamp)

        # Return updated status
        return get_live_event_status_resolver(event_id)
    except Exception as e:
        raise Exception(f"Error checking out student: {e}")


def add_event_custom_data_resolver(event_id: int, data: EventCustomDataInput) -> EventCustomData:
    """Add or update custom data for an event in MongoDB"""
    try:
        # Delete existing custom data
        event_custom_fields.delete_many({"eventId": event_id})

        # Prepare document
        doc = {
            "eventId": event_id,
            "eventTypeId": data.event_type_id,
            "custom_data": data.custom_data
        }

        # Insert new document
        event_custom_fields.insert_one(doc)

        return EventCustomData(
            event_id=event_id,
            event_type_id=data.event_type_id,
            custom_data=data.custom_data
        )
    except Exception as e:
        raise Exception(f"Error adding custom data: {e}")


# ============================================================================
# QUERY TYPE
# ============================================================================

@strawberry.type
class Query:
    """Root query type - all read operations"""

    # People queries
    people: List[Person] = strawberry.field(
        resolver=get_all_people_resolver,
        description="Get all people in the youth group"
    )

    person: Optional[Person] = strawberry.field(
        resolver=get_person_by_id_resolver,
        description="Get a specific person by ID"
    )

    students: List[Person] = strawberry.field(
        resolver=get_all_students_resolver,
        description="Get all students (roleId = 1)"
    )

    # Event queries
    events: List[Event] = strawberry.field(
        resolver=get_all_events_resolver,
        description="Get all events"
    )

    event: Optional[Event] = strawberry.field(
        resolver=get_event_by_id_resolver,
        description="Get a specific event by ID"
    )

    event_registrations: List[Person] = strawberry.field(
        resolver=get_event_registrations_resolver,
        description="Get all people registered for an event"
    )

    # Small group queries
    small_groups: List[SmallGroup] = strawberry.field(
        resolver=get_all_small_groups_resolver,
        description="Get all small groups"
    )

    small_group_members: List[Person] = strawberry.field(
        resolver=get_small_group_members_resolver,
        description="Get all members of a small group"
    )

    # MongoDB queries
    event_custom_data: Optional[EventCustomData] = strawberry.field(
        resolver=get_event_custom_data_resolver,
        description="Get custom data for an event from MongoDB"
    )

    event_with_custom_data: Optional[EventWithCustomData] = strawberry.field(
        resolver=get_event_with_custom_data_resolver,
        description="Get event with its custom MongoDB data combined"
    )

    # Redis queries (live data)
    live_event_status: LiveEventStatus = strawberry.field(
        resolver=get_live_event_status_resolver,
        description="Get real-time check-in status for an event from Redis"
    )

    active_events: List[ActiveEvent] = strawberry.field(
        resolver=get_active_events_resolver,
        description="Get all events with people currently checked in"
    )


# ============================================================================
# MUTATION TYPE
# ============================================================================

@strawberry.type
class Mutation:
    """Root mutation type - all write operations"""

    register_for_event: bool = strawberry.field(
        resolver=register_for_event_resolver,
        description="Register a person for an event"
    )

    check_in_student: LiveEventStatus = strawberry.field(
        resolver=check_in_student_resolver,
        description="Check in a student to an event (updates Redis)"
    )

    check_out_student: LiveEventStatus = strawberry.field(
        resolver=check_out_student_resolver,
        description="Check out a student from an event (updates Redis)"
    )

    add_event_custom_data: EventCustomData = strawberry.field(
        resolver=add_event_custom_data_resolver,
        description="Add or update custom data for an event in MongoDB"
    )


# ============================================================================
# SCHEMA
# ============================================================================

schema = strawberry.Schema(query=Query, mutation=Mutation)