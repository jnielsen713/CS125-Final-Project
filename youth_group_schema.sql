-- Westmont College CS 125 Database Design Fall 2025
-- Final Project Youth Group Database Schema
-- Assistant Professor Mike Ryu
-- Tim Klug and Joshua Nielsen

DROP DATABASE IF EXISTS youth_group_database;
CREATE DATABASE youth_group_database;
USE youth_group_database;


CREATE TABLE Person (
    personId INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(25),
    lastName VARCHAR(25),
    birthday DATE NOT NULL,
    email VARCHAR(50),
    phone VARCHAR(20)
);

CREATE TABLE Role (
    roleId INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Event (
    eventId INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
    type VARCHAR(50),
    startDateTime DATETIME NOT NULL,
    endDateTime DATETIME,
    location VARCHAR(50) NOT NULL
);

CREATE TABLE SmallGroup (
    smallGroupId INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    leaderId SMALLINT UNSIGNED,
    CONSTRAINT fk_small_group_leader FOREIGN KEY (leaderId) REFERENCES Person(personId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE PersonRole (
    personId INT UNSIGNED,
    roleId INT UNSIGNED,
    PRIMARY KEY (personId, roleId),
    CONSTRAINT fk_person_role_person FOREIGN KEY (personId) REFERENCES Person(personId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_person_role_role FOREIGN KEY (roleId) REFERENCES Role(roleId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE ParentChild (
    parentId INT UNSIGNED NOT NULL,
    childId INT UNSIGNED NOT NULL,
    PRIMARY KEY (parentId, childId),
    CONSTRAINT fk_parent_child_personasparent FOREIGN KEY (parentId) REFERENCES Person(personId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_parent_child_personaschild FOREIGN KEY (childId) REFERENCES Person(personId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CHECK (parentId != childId)
);

CREATE TABLE EventRegistration (
    personId INT UNSIGNED NOT NULL,
    eventId INT UNSIGNED NOT NULL,
    registrationDate DATETIME NOT NULL,
    PRIMARY KEY (personId, eventId),
    CONSTRAINT fk_event_registration_to_person FOREIGN KEY (personId) REFERENCES Person(personId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_event_registration_to_event FOREIGN KEY (eventId) REFERENCES Event(eventId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Attendance (
    personId INT UNSIGNED NOT NULL,
    eventId INT UNSIGNED NOT NULL,
    checkedInAt DATETIME NOT NULL,
    checkedOutAt DATETIME,
    PRIMARY KEY (personId, eventId),
    CONSTRAINT fk_attendance_to_person FOREIGN KEY (personId) REFERENCES Person(personId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_attendance_to_event FOREIGN KEY (eventId) REFERENCES Event(eventId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    CHECK (checkedOutAt IS NULL OR checkedOutAt >= checkedInAt)
);

CREATE TABLE SmallGroupMembership (
    studentId INT UNSIGNED NOT NULL,
    smallGroupId INT UNSIGNED NOT NULL,
    joinedDate DATE NOT NULL,
    PRIMARY KEY (studentId, smallGroupId),
    CONSTRAINT fk_small_group_membership_to_personasstudent FOREIGN KEY (studentId) REFERENCES Person(personId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_small_group_membership_to_small_group FOREIGN KEY (smallGroupId) REFERENCES SmallGroup(smallGroupId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE SmallGroupMeeting (
    groupMeetingId INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    smallGroupId INT UNSIGNED NOT NULL,
    dateTime DATETIME NOT NULL,
    notes TEXT,
    CONSTRAINT fk_small_group_meeting_to_small_group FOREIGN KEY (smallGroupId) REFERENCES SmallGroup(smallGroupId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE SmallGroupMeetingAttendance (
    groupMeetingId INT UNSIGNED NOT NULL,
    personId INT UNSIGNED NOT NULL,
    checkedInAt DATETIME NOT NULL,
    checkedOutAt DATETIME,
    PRIMARY KEY (groupMeetingId, personId),
    CONSTRAINT fk_small_group_meeting_attendance_to_smallgroupmeeting FOREIGN KEY (groupMeetingId) REFERENCES SmallGroupMeeting(groupMeetingId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_small_group_meeting_attendance_to_person FOREIGN KEY (personId) REFERENCES Person(personId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CHECK (checkedOutAt IS NULL OR checkedOutAt >= checkedInAt)
);