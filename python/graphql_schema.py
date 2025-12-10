import strawberry
from typing import List, Optional
from datetime import datetime, date

# --- Import our existing data-fetching logic (from db_programming.py) ---
# We'll use the Flask endpoint functions or the underlying logic they use.
# NOTE: We assume the functions in db_programming.py are available to be called.
# In a real Flask app, you'd refactor the core data logic out of the endpoints
# and into a service layer. For simplicity, we assume we can call them directly.

# For this model, we'll assume we can import the core functions like this:
import strawberry
from typing import List, Optional
from datetime import datetime, date

# --- Import our core callable data access layer (from db_programming.py) ---
# Assuming the file structure is now correct and these functions are callable.
from db_programming import (
    get_students,
    get_events_data,  # Using the internal function name for simplicity
    _get_smallgroups_data,
    get_upcoming_events,
    get_event_attendances,
    get_smallgroup_members,
    get_student_parents,
    get_parent_children,
    get_person_registrations,
    get_live_dashboard,

    # Mutations (callable core logic)
    add_student_to_smallgroup,
    remove_student_from_smallgroup,
    register_for_event,
    unregister_from_event,
    checkin_student,
    checkout_student,
    finalize_event_attendance,

    # MongoDB access: We need the custom data access function
    event_custom_fields  # Access to the MongoDB collection object
)


# --- Type Definitions (MySQL Core Data) ---

@strawberry.type
class Person:
    """GraphQL type representing a Person (Student, Leader, Parent, Volunteer)."""
    personId: int
    firstName: str
    lastName: str
    birthday: Optional[date]
    email: Optional[str]
    phone: Optional[str]


@strawberry.type
class Event:
    """GraphQL type representing an Event."""
    eventId: int
    eventName: str
    eventTypeId: int
    startDateTime: datetime
    endDateTime: Optional[datetime]
    location: str

    # Custom data field (from MongoDB)
    @strawberry.field(description="Fetches custom, unstructured data for this event from MongoDB.")
    def custom_data(self) -> Optional[object]:
        # 'self' is the Event object returned by the resolver (which has eventId)
        doc = event_custom_fields.find_one({"eventId": self.eventId}, {"_id": 0, "custom_data": 1})
        return doc.get('custom_data') if doc else None


@strawberry.type
class SmallGroup:
    """GraphQL type representing a Small Group."""
    smallGroupId: int
    name: str
    description: Optional[str]
    leaderId: int


# --- Type Definitions (Relationship & Attendance Data) ---

@strawberry.type
class SmallGroupMember:
    """GraphQL type for a student in a small group (includes join date)."""
    personId: int
    firstName: str
    lastName: str
    email: Optional[str]
    phone: Optional[str]
    joinedDate: date


@strawberry.type
class EventAttendance:
    """GraphQL type for attendance record of a person at an event."""
    personId: int
    firstName: str
    lastName: str
    checkedInAt: datetime
    checkedOutAt: Optional[datetime]


@strawberry.type
class EventRegistration:
    """GraphQL type for an event registration record."""
    eventId: int
    eventName: str
    startDateTime: datetime
    location: str
    registrationDate: datetime


# --- Type Definitions (Multi-Database / Live Data) ---

@strawberry.type
class LiveEventStudent:
    """Nested type for a student currently checked in (from Redis + MySQL join)."""
    id: int
    name: str


@strawberry.type
class LiveActiveEvent:
    """Type for a single active event (Redis + MySQL)."""
    event_id: int
    event_name: str
    event_type: int
    start_time: datetime
    location: str
    current_attendance: int
    students: List[LiveEventStudent]

    # Nested field to grab MongoDB data for the active event (Tri-database join)
    @strawberry.field(description="Fetches custom, unstructured data for this active event from MongoDB.")
    def custom_data(self) -> Optional[object]:
        # 'self' is the LiveActiveEvent object which has event_id
        doc = event_custom_fields.find_one({"eventId": self.event_id}, {"_id": 0, "custom_data": 1})
        return doc.get('custom_data') if doc else None


@strawberry.type
class LiveDashboard:
    """
    The top-level type for the live admin dashboard (MySQL + Redis).
    """
    timestamp: datetime
    active_events: List[LiveActiveEvent]
    total_people_across_all_events: int
    number_of_active_events: int


# --- Helper Resolver: Maps Raw SQL Tuple Data to Strawberry Types ---
def map_person_data(data) -> Person:
    """Maps a standard 6-tuple/list person record from MySQL into the Person type."""
    if not data:
        return None
    # Data is expected to be a tuple: (personId, firstName, lastName, email, phone, birthday)
    return Person(
        personId=data[0],
        firstName=data[1],
        lastName=data[2],
        email=data[3] if len(data) > 3 else None,
        phone=data[4] if len(data) > 4 else None,
        birthday=data[5].date() if len(data) > 5 and isinstance(data[5], datetime) else (
            data[5] if len(data) > 5 else None)
    )


def map_event_data(data) -> Event:
    """Maps a standard 6-tuple/list event record from MySQL into the Event type."""
    if not data:
        return None
    # Data is expected to be a tuple: (eventId, eventName, eventTypeId, startDateTime, endDateTime, location)
    return Event(
        eventId=data[0],
        eventName=data[1],
        eventTypeId=data[2],
        startDateTime=data[3],
        endDateTime=data[4],
        location=data[5]
    )


# --- Query Resolvers (Read Operations) ---
@strawberry.type
class Query:
    """
    Defines all the queries (read operations) available in the Youth Group GraphQL API.
    """

    @strawberry.field(description="Retrieve a list of all students (roleId = 1).")
    def all_students(self) -> List[Person]:
        students_data = get_students()
        return [map_person_data(s) for s in students_data]

    @strawberry.field(description="Retrieve all small groups.")
    def all_small_groups(self) -> List[SmallGroup]:
        # _get_smallgroups_data returns (smallGroupId, name, description, leaderId)
        rows = _get_smallgroups_data()
        return [SmallGroup(
            smallGroupId=r[0],
            name=r[1],
            description=r[2],
            leaderId=r[3]
        ) for r in rows]

    @strawberry.field(description="Retrieve all events (including custom data from MongoDB).")
    def all_events(self) -> List[Event]:
        rows = get_events_data()
        # Uses the Event type which has the MongoDB resolver built-in
        return [map_event_data(r) for r in rows]

    @strawberry.field(description="Retrieve all events scheduled for the future.")
    def upcoming_events(self) -> List[Event]:
        rows = get_upcoming_events()
        return [map_event_data(r) for r in rows]

    @strawberry.field(description="Retrieve an event's attendance records (MySQL).")
    def event_attendance_history(self, eventId: int) -> List[EventAttendance]:
        attendance_data = get_event_attendances(eventId)
        return [
            EventAttendance(
                personId=a[0],
                firstName=a[1],
                lastName=a[2],
                checkedInAt=a[3],
                checkedOutAt=a[4]
            ) for a in attendance_data
        ]

    @strawberry.field(description="Retrieve members of a specific small group (MySQL).")
    def small_group_members(self, groupId: int) -> List[SmallGroupMember]:
        members_data = get_smallgroup_members(groupId)
        return [
            SmallGroupMember(
                personId=m[0],
                firstName=m[1],
                lastName=m[2],
                email=m[3],
                phone=m[4],
                joinedDate=m[5].date()  # Convert datetime to date
            ) for m in members_data
        ]

    @strawberry.field(description="Get the comprehensive live attendance dashboard (Redis + MySQL + MongoDB).")
    def live_dashboard(self) -> LiveDashboard:
        # get_live_dashboard returns a dictionary structure (result, status)
        data, _ = get_live_dashboard()

        active_events = []
        for event in data.get("active_events", []):
            live_students = [LiveEventStudent(**s) for s in event.get("students", [])]
            # Must convert to LiveActiveEvent for the nested MongoDB resolver to work
            active_events.append(
                LiveActiveEvent(
                    event_id=event.get("event_id"),
                    event_name=event.get("event_name"),
                    event_type=event.get("event_type"),
                    start_time=datetime.fromisoformat(event.get("start_time")) if event.get("start_time") else None,
                    location=event.get("location"),
                    current_attendance=event.get("current_attendance"),
                    students=live_students
                )
            )

        return LiveDashboard(
            timestamp=datetime.fromisoformat(data.get("timestamp")),
            active_events=active_events,
            total_people_across_all_events=data.get("total_people_across_all_events"),
            number_of_active_events=data.get("number_of_active_events")
        )


# --- Mutation Resolvers (Write Operations) ---

# Define an input type for small group addition/removal
@strawberry.input
class SmallGroupMembershipInput:
    groupId: int
    studentId: int


# Define an input type for event check-in/out
@strawberry.input
class EventCheckinInput:
    eventId: int
    studentId: int


@strawberry.input
class EventRegistrationInput:
    eventId: int
    personId: int


@strawberry.type
class MutationResult:
    """A generic type for mutation responses."""
    success: bool
    message: str
    details: Optional[str] = None


@strawberry.type
class Mutation:
    """
    Defines all the mutations (write operations) available in the Youth Group GraphQL API.
    """

    @strawberry.mutation(description="Add a student to a small group (MySQL).")
    def add_student_to_group(self, input: SmallGroupMembershipInput) -> MutationResult:
        result, status = add_student_to_smallgroup(input.groupId, input.studentId)
        return MutationResult(
            success=result.get("success", False),
            message=result.get("message", result.get("error", "An unknown error occurred")),
            details=f"HTTP Status: {status}"
        )

    @strawberry.mutation(description="Remove a student from a small group (MySQL).")
    def remove_student_from_group(self, input: SmallGroupMembershipInput) -> MutationResult:
        result, status = remove_student_from_smallgroup(input.groupId, input.studentId)
        return MutationResult(
            success=result.get("success", False),
            message=result.get("message", result.get("error", "An unknown error occurred")),
            details=f"HTTP Status: {status}"
        )

    @strawberry.mutation(description="Register a person for an event (MySQL).")
    def register_person_for_event(self, input: EventRegistrationInput) -> MutationResult:
        result, status = register_for_event(input.eventId, input.personId)
        return MutationResult(
            success=result.get("success", False),
            message=result.get("message", result.get("error", "An unknown error occurred")),
            details=f"Registration Date: {result.get('registration_date')}"
        )

    @strawberry.mutation(description="Unregister a person from an event (MySQL).")
    def unregister_person_from_event(self, input: EventRegistrationInput) -> MutationResult:
        result, status = unregister_from_event(input.eventId, input.personId)
        return MutationResult(
            success=result.get("success", False),
            message=result.get("message", result.get("error", "An unknown error occurred")),
            details=f"HTTP Status: {status}"
        )

    @strawberry.mutation(description="Check in a student to an event in real-time (Redis).")
    def check_in_student(self, input: EventCheckinInput) -> MutationResult:
        result, status = checkin_student(input.eventId, input.studentId)
        return MutationResult(
            success=result.get("success", False),
            message=result.get("message", f"Current Attendance: {result.get('current_attendance', 'N/A')}"),
            details=f"Checked in at: {result.get('checked_in_at')}"
        )

    @strawberry.mutation(description="Check out a student from an event (Redis).")
    def check_out_student(self, input: EventCheckinInput) -> MutationResult:
        result, status = checkout_student(input.eventId, input.studentId)
        return MutationResult(
            success=result.get("success", False),
            message=result.get("message", f"Current Attendance: {result.get('current_attendance', 'N/A')}"),
            details=f"Checked out at: {result.get('checked_out_at')}"
        )

    @strawberry.mutation(description="Finalize event attendance from Redis to MySQL.")
    def finalize_attendance(self, eventId: int) -> MutationResult:
        result, status = finalize_event_attendance(eventId)
        return MutationResult(
            success=result.get("success", False),
            message=result.get("message"),
            details=f"Records saved to MySQL: {result.get('records_saved', 0)}"
        )


# --- Schema ---
# This is the final step where we create the actual GraphQL schema.
schema = strawberry.Schema(query=Query, mutation=Mutation)