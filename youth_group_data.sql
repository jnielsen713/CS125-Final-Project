-- Westmont College CS 125 Database Design Fall 2025
-- Final Project Youth Group Database Schema
-- Assistant Professor Mike Ryu
-- Tim Klug and Joshua Nielsen
-- NOTE: This data is FICTIONAL, and does not represent real people or events

USE youth_group_database;

-- ============================================================================
-- ROLES
-- ============================================================================

INSERT INTO Role (name) VALUES
    ('Student'),
    ('Parent'),
    ('Leader'),
    ('Volunteer');

-- ============================================================================
-- PEOPLE
-- ============================================================================

-- Leaders & Staff (IDs 1-5)
INSERT INTO Person (firstName, lastName, birthday, email, phone) VALUES
    ('Sarah', 'Johnson', '1985-03-15', 'sarah.johnson@church.org', '555-0101'),
    ('Michael', 'Chen', '1988-07-22', 'michael.chen@church.org', '555-0102'),
    ('Jessica', 'Rodriguez', '1990-11-08', 'jessica.rod@church.org', '555-0103'),
    ('David', 'Thompson', '1982-05-30', 'david.thompson@church.org', '555-0104'),
    ('Emily', 'Martinez', '1992-09-14', 'emily.martinez@church.org', '555-0105');

-- Volunteers (IDs 6-10)
INSERT INTO Person (firstName, lastName, birthday, email, phone) VALUES
    ('Robert', 'Anderson', '1995-02-18', 'rob.anderson@email.com', '555-0106'),
    ('Amanda', 'Wilson', '1998-06-25', 'amanda.wilson@email.com', '555-0107'),
    ('Christopher', 'Lee', '1993-12-03', 'chris.lee@email.com', '555-0108'),
    ('Jennifer', 'Taylor', '1996-04-17', 'jen.taylor@email.com', '555-0109'),
    ('Brandon', 'White', '1994-08-29', 'brandon.white@email.com', '555-0110');

-- High School Students (IDs 11-25)
INSERT INTO Person (firstName, lastName, birthday, email, phone) VALUES
    ('Emma', 'Davis', '2008-01-12', 'emma.davis@email.com', '555-0201'),
    ('Noah', 'Garcia', '2007-03-28', 'noah.garcia@email.com', '555-0202'),
    ('Olivia', 'Miller', '2008-05-19', 'olivia.miller@email.com', '555-0203'),
    ('Liam', 'Brown', '2007-09-07', 'liam.brown@email.com', '555-0204'),
    ('Sophia', 'Jones', '2008-11-22', 'sophia.jones@email.com', '555-0205'),
    ('Ethan', 'Williams', '2007-02-14', 'ethan.williams@email.com', '555-0206'),
    ('Ava', 'Martinez', '2008-07-30', 'ava.martinez@email.com', '555-0207'),
    ('Mason', 'Anderson', '2007-12-05', 'mason.anderson@email.com', '555-0208'),
    ('Isabella', 'Thomas', '2008-04-18', 'isabella.thomas@email.com', '555-0209'),
    ('Lucas', 'Jackson', '2007-08-26', 'lucas.jackson@email.com', '555-0210'),
    ('Mia', 'Harris', '2008-10-09', 'mia.harris@email.com', '555-0211'),
    ('Alexander', 'Clark', '2007-06-15', 'alex.clark@email.com', '555-0212'),
    ('Charlotte', 'Lewis', '2008-09-03', 'charlotte.lewis@email.com', '555-0213'),
    ('James', 'Walker', '2007-11-20', 'james.walker@email.com', '555-0214'),
    ('Amelia', 'Hall', '2008-03-08', 'amelia.hall@email.com', '555-0215');

-- Middle School Students (IDs 26-40)
INSERT INTO Person (firstName, lastName, birthday, email, phone) VALUES
    ('Benjamin', 'Young', '2010-02-25', 'ben.young@email.com', '555-0301'),
    ('Harper', 'King', '2011-05-12', 'harper.king@email.com', '555-0302'),
    ('Logan', 'Wright', '2010-08-30', 'logan.wright@email.com', '555-0303'),
    ('Evelyn', 'Lopez', '2011-01-17', 'evelyn.lopez@email.com', '555-0304'),
    ('Jackson', 'Hill', '2010-06-08', 'jackson.hill@email.com', '555-0305'),
    ('Abigail', 'Scott', '2011-09-22', 'abby.scott@email.com', '555-0306'),
    ('Sebastian', 'Green', '2010-03-14', 'sebastian.green@email.com', '555-0307'),
    ('Emily', 'Adams', '2011-07-29', 'emily.adams@email.com', '555-0308'),
    ('Aiden', 'Baker', '2010-11-05', 'aiden.baker@email.com', '555-0309'),
    ('Sofia', 'Nelson', '2011-04-19', 'sofia.nelson@email.com', '555-0310'),
    ('Matthew', 'Carter', '2010-12-27', 'matt.carter@email.com', '555-0311'),
    ('Grace', 'Mitchell', '2011-02-11', 'grace.mitchell@email.com', '555-0312'),
    ('Daniel', 'Perez', '2010-07-06', 'daniel.perez@email.com', '555-0313'),
    ('Chloe', 'Roberts', '2011-10-23', 'chloe.roberts@email.com', '555-0314'),
    ('Henry', 'Turner', '2010-05-16', 'henry.turner@email.com', '555-0315');

-- Parents (IDs 41-70)
INSERT INTO Person (firstName, lastName, birthday, email, phone) VALUES
    ('John', 'Davis', '1978-04-22', 'john.davis@email.com', '555-0401'),
    ('Michelle', 'Davis', '1980-08-15', 'michelle.davis@email.com', '555-0402'),
    ('Carlos', 'Garcia', '1975-11-30', 'carlos.garcia@email.com', '555-0403'),
    ('Lisa', 'Garcia', '1977-03-09', 'lisa.garcia@email.com', '555-0404'),
    ('Steven', 'Miller', '1979-07-14', 'steven.miller@email.com', '555-0405'),
    ('Rachel', 'Miller', '1981-12-28', 'rachel.miller@email.com', '555-0406'),
    ('Thomas', 'Brown', '1976-02-05', 'thomas.brown@email.com', '555-0407'),
    ('Patricia', 'Brown', '1978-09-19', 'patricia.brown@email.com', '555-0408'),
    ('Kevin', 'Jones', '1980-06-11', 'kevin.jones@email.com', '555-0409'),
    ('Angela', 'Jones', '1982-01-24', 'angela.jones@email.com', '555-0410'),
    ('Mark', 'Williams', '1977-10-07', 'mark.williams@email.com', '555-0411'),
    ('Jennifer', 'Williams', '1979-05-20', 'jennifer.williams@email.com', '555-0412'),
    ('Daniel', 'Martinez', '1981-08-03', 'dan.martinez@email.com', '555-0413'),
    ('Laura', 'Martinez', '1983-11-16', 'laura.martinez@email.com', '555-0414'),
    ('Paul', 'Anderson', '1974-03-29', 'paul.anderson@email.com', '555-0415'),
    ('Sandra', 'Anderson', '1976-12-12', 'sandra.anderson@email.com', '555-0416'),
    ('Richard', 'Thomas', '1978-07-25', 'richard.thomas@email.com', '555-0417'),
    ('Nancy', 'Thomas', '1980-02-08', 'nancy.thomas@email.com', '555-0418'),
    ('Brian', 'Jackson', '1979-09-14', 'brian.jackson@email.com', '555-0419'),
    ('Karen', 'Jackson', '1981-04-27', 'karen.jackson@email.com', '555-0420'),
    ('Jeffrey', 'Harris', '1975-11-02', 'jeff.harris@email.com', '555-0421'),
    ('Elizabeth', 'Harris', '1977-06-15', 'liz.harris@email.com', '555-0422'),
    ('Joseph', 'Clark', '1980-01-19', 'joe.clark@email.com', '555-0423'),
    ('Mary', 'Clark', '1982-08-22', 'mary.clark@email.com', '555-0424'),
    ('Andrew', 'Lewis', '1976-05-06', 'andrew.lewis@email.com', '555-0425'),
    ('Susan', 'Lewis', '1978-10-29', 'susan.lewis@email.com', '555-0426'),
    ('Joshua', 'Walker', '1979-03-13', 'josh.walker@email.com', '555-0427'),
    ('Barbara', 'Walker', '1981-12-26', 'barbara.walker@email.com', '555-0428'),
    ('Christopher', 'Hall', '1977-07-09', 'chris.hall@email.com', '555-0429'),
    ('Margaret', 'Hall', '1979-02-21', 'margaret.hall@email.com', '555-0430');

-- ============================================================================
-- PERSON ROLES
-- ============================================================================

-- Leaders
INSERT INTO PersonRole (personId, roleId) VALUES
    (1, 3), -- Sarah Johnson: Leader
    (2, 3), -- Michael Chen: Leader
    (3, 3), -- Jessica Rodriguez: Leader
    (4, 3), -- David Thompson: Leader
    (5, 3); -- Emily Martinez: Leader

-- Volunteers
INSERT INTO PersonRole (personId, roleId) VALUES
    (6, 4), -- Robert Anderson: Volunteer
    (7, 4), -- Amanda Wilson: Volunteer
    (8, 4), -- Christopher Lee: Volunteer
    (9, 4), -- Jennifer Taylor: Volunteer
    (10, 4); -- Brandon White: Volunteer

-- High School Students
INSERT INTO PersonRole (personId, roleId) VALUES
    (11, 1), (12, 1), (13, 1), (14, 1), (15, 1),
    (16, 1), (17, 1), (18, 1), (19, 1), (20, 1),
    (21, 1), (22, 1), (23, 1), (24, 1), (25, 1);

-- Middle School Students
INSERT INTO PersonRole (personId, roleId) VALUES
    (26, 1), (27, 1), (28, 1), (29, 1), (30, 1),
    (31, 1), (32, 1), (33, 1), (34, 1), (35, 1),
    (36, 1), (37, 1), (38, 1), (39, 1), (40, 1);

-- Parents
INSERT INTO PersonRole (personId, roleId) VALUES
    (41, 2), (42, 2), (43, 2), (44, 2), (45, 2),
    (46, 2), (47, 2), (48, 2), (49, 2), (50, 2),
    (51, 2), (52, 2), (53, 2), (54, 2), (55, 2),
    (56, 2), (57, 2), (58, 2), (59, 2), (60, 2),
    (61, 2), (62, 2), (63, 2), (64, 2), (65, 2),
    (66, 2), (67, 2), (68, 2), (69, 2), (70, 2);

-- ============================================================================
-- PARENT-CHILD RELATIONSHIPS
-- ============================================================================

INSERT INTO ParentChild (parentId, childId) VALUES
    -- Emma Davis (11)
    (41, 11), (42, 11),
    -- Noah Garcia (12)
    (43, 12), (44, 12),
    -- Olivia Miller (13)
    (45, 13), (46, 13),
    -- Liam Brown (14)
    (47, 14), (48, 14),
    -- Sophia Jones (15)
    (49, 15), (50, 15),
    -- Ethan Williams (16)
    (51, 16), (52, 16),
    -- Ava Martinez (17)
    (53, 17), (54, 17),
    -- Mason Anderson (18)
    (55, 18), (56, 18),
    -- Isabella Thomas (19)
    (57, 19), (58, 19),
    -- Lucas Jackson (20)
    (59, 20), (60, 20),
    -- Mia Harris (21)
    (61, 21), (62, 21),
    -- Alexander Clark (22)
    (63, 22), (64, 22),
    -- Charlotte Lewis (23)
    (65, 23), (66, 23),
    -- James Walker (24)
    (67, 24), (68, 24),
    -- Amelia Hall (25)
    (69, 25), (70, 25),
    -- Benjamin Young (26)
    (41, 26), (42, 26),
    -- Harper King (27)
    (43, 27), (44, 27),
    -- Logan Wright (28)
    (45, 28), (46, 28),
    -- Evelyn Lopez (29)
    (47, 29), (48, 29),
    -- Jackson Hill (30)
    (49, 30), (50, 30),
    -- Abigail Scott (31)
    (51, 31), (52, 31),
    -- Sebastian Green (32)
    (53, 32), (54, 32),
    -- Emily Adams (33)
    (55, 33), (56, 33),
    -- Aiden Baker (34)
    (57, 34), (58, 34),
    -- Sofia Nelson (35)
    (59, 35), (60, 35),
    -- Matthew Carter (36)
    (61, 36), (62, 36),
    -- Grace Mitchell (37)
    (63, 37), (64, 37),
    -- Daniel Perez (38)
    (65, 38), (66, 38),
    -- Chloe Roberts (39)
    (67, 39), (68, 39),
    -- Henry Turner (40)
    (69, 40), (70, 40);

-- ============================================================================
-- SMALL GROUPS
-- ============================================================================

INSERT INTO SmallGroup (name, description, leaderId) VALUES
    ('High School Boys', 'Small group for high school boys focusing on faith and leadership', 2),
    ('High School Girls', 'Small group for high school girls exploring identity and faith', 1),
    ('Middle School Boys', 'Fun and faith-based group for middle school boys', 4),
    ('Middle School Girls', 'Creative small group for middle school girls', 3),
    ('Freshmen Connect', 'Helping freshmen transition to high school and deepen their faith', 5);

-- ============================================================================
-- SMALL GROUP MEMBERSHIP
-- ============================================================================

-- High School Boys (Group 1)
INSERT INTO SmallGroupMembership (studentId, smallGroupId, joinedDate) VALUES
    (12, 1, '2025-09-01'), -- Noah
    (14, 1, '2025-09-01'), -- Liam
    (16, 1, '2025-09-08'), -- Ethan
    (18, 1, '2025-09-01'), -- Mason
    (20, 1, '2025-09-15'), -- Lucas
    (22, 1, '2025-09-01'), -- Alexander
    (24, 1, '2025-09-01'); -- James

-- High School Girls (Group 2)
INSERT INTO SmallGroupMembership (studentId, smallGroupId, joinedDate) VALUES
    (11, 2, '2025-09-01'), -- Emma
    (13, 2, '2025-09-01'), -- Olivia
    (15, 2, '2025-09-08'), -- Sophia
    (17, 2, '2025-09-01'), -- Ava
    (19, 2, '2025-09-01'), -- Isabella
    (21, 2, '2025-09-15'), -- Mia
    (23, 2, '2025-09-01'), -- Charlotte
    (25, 2, '2025-09-08'); -- Amelia

-- Middle School Boys (Group 3)
INSERT INTO SmallGroupMembership (studentId, smallGroupId, joinedDate) VALUES
    (26, 3, '2025-09-01'), -- Benjamin
    (28, 3, '2025-09-08'), -- Logan
    (30, 3, '2025-09-01'), -- Jackson
    (32, 3, '2025-09-15'), -- Sebastian
    (34, 3, '2025-09-01'), -- Aiden
    (36, 3, '2025-09-01'), -- Matthew
    (38, 3, '2025-09-08'); -- Daniel

-- Middle School Girls (Group 4)
INSERT INTO SmallGroupMembership (studentId, smallGroupId, joinedDate) VALUES
    (27, 4, '2025-09-01'), -- Harper
    (29, 4, '2025-09-01'), -- Evelyn
    (31, 4, '2025-09-08'), -- Abigail
    (33, 4, '2025-09-15'), -- Emily
    (35, 4, '2025-09-01'), -- Sofia
    (37, 4, '2025-09-01'), -- Grace
    (39, 4, '2025-09-08'); -- Chloe

-- Freshmen Connect (Group 5) - mixed gender
INSERT INTO SmallGroupMembership (studentId, smallGroupId, joinedDate) VALUES
    (11, 5, '2025-09-01'), -- Emma
    (12, 5, '2025-09-01'), -- Noah
    (13, 5, '2025-09-01'), -- Olivia
    (14, 5, '2025-09-01'), -- Liam
    (15, 5, '2025-09-08'); -- Sophia

-- ============================================================================
-- SMALL GROUP MEETINGS
-- ============================================================================

-- High School Boys - Weekly Tuesday meetings
INSERT INTO SmallGroupMeeting (smallGroupId, dateTime, notes) VALUES
    (1, '2025-09-09 19:00:00', 'First meeting of the year! Discussed goals and got to know each other.'),
    (1, '2025-09-16 19:00:00', 'Talked about handling peer pressure. Great discussion.'),
    (1, '2025-09-23 19:00:00', 'Leadership series part 1 - What makes a good leader?'),
    (1, '2025-09-30 19:00:00', 'Leadership series part 2 - Leading by example.'),
    (1, '2025-10-07 19:00:00', 'Sports and faith - how they connect.'),
    (1, '2025-10-14 19:00:00', 'Small group service project planning.'),
    (1, '2025-10-21 19:00:00', 'Discussing dating and relationships from a faith perspective.'),
    (1, '2025-10-28 19:00:00', 'Game night! Pizza and board games.'),
    (1, '2025-11-04 19:00:00', 'What does it mean to be a man of faith?'),
    (1, '2025-11-11 19:00:00', 'Gratitude discussion - what are we thankful for?'),
    (1, '2025-11-18 19:00:00', 'Planning for the winter retreat.');

-- High School Girls - Weekly Wednesday meetings
INSERT INTO SmallGroupMeeting (smallGroupId, dateTime, notes) VALUES
    (2, '2025-09-10 19:00:00', 'Welcome back! Shared summer highlights and set group expectations.'),
    (2, '2025-09-17 19:00:00', 'Identity in Christ - who does God say we are?'),
    (2, '2025-09-24 19:00:00', 'Social media and self-image. Vulnerable and honest conversation.'),
    (2, '2025-10-01 19:00:00', 'Friendship dynamics and drama - how to navigate well.'),
    (2, '2025-10-08 19:00:00', 'Worship night with acoustic music.'),
    (2, '2025-10-15 19:00:00', 'Body image and cultural pressures.'),
    (2, '2025-10-22 19:00:00', 'Movie night - watched faith-based film and discussed.'),
    (2, '2025-10-29 19:00:00', 'Finding your voice - speaking up for what matters.'),
    (2, '2025-11-05 19:00:00', 'Prayer and journaling night.'),
    (2, '2025-11-12 19:00:00', 'Thanksgiving prep - discussed gratitude practices.'),
    (2, '2025-11-19 19:00:00', 'Planning secret sister gift exchange for December.');

-- Middle School Boys - Weekly Thursday meetings
INSERT INTO SmallGroupMeeting (smallGroupId, dateTime, notes) VALUES
    (3, '2025-09-11 18:30:00', 'Kickoff night with pizza and games!'),
    (3, '2025-09-18 18:30:00', 'What is faith? Basic concepts discussion.'),
    (3, '2025-09-25 18:30:00', 'Video game night with faith conversations.'),
    (3, '2025-10-02 18:30:00', 'Dealing with bullies and standing up for others.'),
    (3, '2025-10-09 18:30:00', 'Outdoor scavenger hunt with devotional.'),
    (3, '2025-10-16 18:30:00', 'Heroes of the Bible - David and Goliath.'),
    (3, '2025-10-23 18:30:00', 'Sports night - basketball and faith talk.'),
    (3, '2025-10-30 18:30:00', 'Halloween alternative party.'),
    (3, '2025-11-06 18:30:00', 'Service project - made care packages for homeless.'),
    (3, '2025-11-13 18:30:00', 'Why prayer matters.'),
    (3, '2025-11-20 18:30:00', 'Thanksgiving feast together!');

-- Middle School Girls - Weekly Thursday meetings
INSERT INTO SmallGroupMeeting (smallGroupId, dateTime, notes) VALUES
    (4, '2025-09-11 18:30:00', 'Craft night! Made friendship bracelets.'),
    (4, '2025-09-18 18:30:00', 'You are loved - Gods love for us.'),
    (4, '2025-09-25 18:30:00', 'Dealing with mean girls and cliques.'),
    (4, '2025-10-02 18:30:00', 'Baking night - made cookies and talked about sharing.'),
    (4, '2025-10-09 18:30:00', 'Comparison trap - being content with who you are.'),
    (4, '2025-10-16 18:30:00', 'Painting night with worship music.'),
    (4, '2025-10-23 18:30:00', 'Stories of brave women in the Bible.'),
    (4, '2025-10-30 18:30:00', 'Fall festival fun night.'),
    (4, '2025-11-06 18:30:00', 'Kindness challenge kickoff.'),
    (4, '2025-11-13 18:30:00', 'Gratitude jars craft.'),
    (4, '2025-11-20 18:30:00', 'Thanksgiving potluck!');

-- Freshmen Connect - Weekly Sunday evenings
INSERT INTO SmallGroupMeeting (smallGroupId, dateTime, notes) VALUES
    (5, '2025-09-07 18:00:00', 'First meeting! High school survival guide discussion.'),
    (5, '2025-09-14 18:00:00', 'Making good choices in high school.'),
    (5, '2025-09-21 18:00:00', 'Time management and balancing school with faith.'),
    (5, '2025-09-28 18:00:00', 'Finding your place - clubs, sports, and community.'),
    (5, '2025-10-05 18:00:00', 'Handling academic pressure.'),
    (5, '2025-10-12 18:00:00', 'Building healthy friendships.'),
    (5, '2025-10-19 18:00:00', 'Game night bonding.'),
    (5, '2025-10-26 18:00:00', 'Dealing with change and transitions.'),
    (5, '2025-11-02 18:00:00', 'Study skills and asking for help.'),
    (5, '2025-11-09 18:00:00', 'Looking ahead - planning for rest of the year.'),
    (5, '2025-11-16 18:00:00', 'Thanksgiving reflection and group celebration.');

-- ============================================================================
-- EVENTS
-- ============================================================================

INSERT INTO Event (eventName, type, startDateTime, endDateTime, location) VALUES
    ('Fall Kickoff BBQ', 'Social', '2025-09-06 17:00:00', '2025-09-06 20:00:00', 'Church Pavilion'),
    ('Parent Info Night', 'Meeting', '2025-09-12 19:00:00', '2025-09-12 21:00:00', 'Fellowship Hall'),
    ('Worship Night', 'Worship', '2025-09-20 19:00:00', '2025-09-20 21:30:00', 'Sanctuary'),
    ('Community Service Day', 'Service', '2025-09-28 09:00:00', '2025-09-28 15:00:00', 'Local Food Bank'),
    ('Movie Night', 'Social', '2025-10-04 18:30:00', '2025-10-04 22:00:00', 'Youth Room'),
    ('Fall Retreat', 'Retreat', '2025-10-18 15:00:00', '2025-10-20 14:00:00', 'Camp Pinewood'),
    ('Halloween Alternative', 'Social', '2025-10-31 18:00:00', '2025-10-31 21:00:00', 'Church Gym'),
    ('Thanksgiving Dinner', 'Social', '2025-11-22 17:00:00', '2025-11-22 20:00:00', 'Fellowship Hall'),
    ('Advent Workshop', 'Workshop', '2025-11-29 14:00:00', '2025-11-29 17:00:00', 'Activities Center'),
    ('Christmas Party', 'Social', '2025-12-13 18:00:00', '2025-12-13 21:00:00', 'Fellowship Hall'),
    ('New Year Lock-in', 'Social', '2025-12-31 20:00:00', '2026-01-01 08:00:00', 'Youth Building');

-- ============================================================================
-- EVENT REGISTRATIONS
-- ============================================================================

-- Fall Kickoff BBQ - Most students registered
INSERT INTO EventRegistration (personId, eventId, registrationDate) VALUES
    (11, 1, '2025-09-01 10:23:00'), (12, 1, '2025-09-01 11:15:00'),
    (13, 1, '2025-09-02 09:45:00'), (14, 1, '2025-09-02 14:30:00'),
    (15, 1, '2025-09-01 16:20:00'), (16, 1, '2025-09-03 08:15:00'),
    (17, 1, '2025-09-01 19:05:00'), (18, 1, '2025-09-02 12:40:00'),
    (19, 1, '2025-09-03 15:55:00'), (20, 1, '2025-09-01 13:10:00'),
    (21, 1, '2025-09-02 17:25:00'), (22, 1, '2025-09-03 10:00:00'),
    (26, 1, '2025-09-01 14:45:00'), (27, 1, '2025-09-02 11:20:00'),
    (28, 1, '2025-09-01 18:30:00'), (30, 1, '2025-09-03 09:15:00');

-- Parent Info Night - Parents registered
INSERT INTO EventRegistration (personId, eventId, registrationDate) VALUES
    (41, 2, '2025-09-05 19:30:00'), (42, 2, '2025-09-05 19:31:00'),
    (43, 2, '2025-09-06 08:45:00'), (44, 2, '2025-09-06 08:46:00'),
    (45, 2, '2025-09-07 12:20:00'), (47, 2, '2025-09-08 15:10:00'),
    (49, 2, '2025-09-07 18:40:00'), (51, 2, '2025-09-08 09:25:00');

-- Worship Night - Mix of students
INSERT INTO EventRegistration (personId, eventId, registrationDate) VALUES
    (11, 3, '2025-09-15 14:20:00'), (13, 3, '2025-09-16 10:30:00'),
    (15, 3, '2025-09-15 19:45:00'), (17, 3, '2025-09-17 08:15:00'),
    (19, 3, '2025-09-18 16:20:00'), (21, 3, '2025-09-16 13:40:00'),
    (23, 3, '2025-09-17 11:05:00'), (25, 3, '2025-09-18 15:30:00'),
    (12, 3, '2025-09-16 09:20:00'), (14, 3, '2025-09-17 14:15:00');

-- Fall Retreat - Major event, many registrations
INSERT INTO EventRegistration (personId, eventId, registrationDate) VALUES
    (11, 6, '2025-10-01 10:15:00'), (12, 6, '2025-10-01 10:20:00'),
    (13, 6, '2025-10-02 14:30:00'), (14, 6, '2025-10-01 11:45:00'),
    (15, 6, '2025-10-03 09:20:00'), (16, 6, '2025-10-01 16:10:00'),
    (17, 6, '2025-10-02 08:40:00'), (18, 6, '2025-10-03 13:25:00'),
    (19, 6, '2025-10-01 15:05:00'), (20, 6, '2025-10-02 11:30:00'),
    (21, 6, '2025-10-03 10:15:00'), (22, 6, '2025-10-01 12:50:00'),
    (23, 6, '2025-10-02 16:20:00'), (24, 6, '2025-10-03 09:45:00'),
    (25, 6, '2025-10-01 14:30:00'), (26, 6, '2025-10-02 10:10:00'),
    (27, 6, '2025-10-03 15:40:00'), (28, 6, '2025-10-01 13:15:00');

-- Thanksgiving Dinner - Recent event
INSERT INTO EventRegistration (personId, eventId, registrationDate) VALUES
    (11, 8, '2025-11-10 14:20:00'), (12, 8, '2025-11-11 09:30:00'),
    (13, 8, '2025-11-10 16:45:00'), (14, 8, '2025-11-12 08:15:00'),
    (15, 8, '2025-11-11 12:40:00'), (17, 8, '2025-11-13 10:25:00'),
    (19, 8, '2025-11-12 15:30:00'), (21, 8, '2025-11-14 09:10:00'),
    (26, 8, '2025-11-11 14:55:00'), (28, 8, '2025-11-13 11:20:00'),
    (30, 8, '2025-11-12 16:40:00'), (32, 8, '2025-11-14 08:50:00');

-- ============================================================================
-- ATTENDANCE RECORDS
-- ============================================================================

-- Fall Kickoff BBQ - High attendance
INSERT INTO Attendance (personId, eventId, checkedInAt, checkedOutAt) VALUES
    (11, 1, '2025-09-06 17:15:00', '2025-09-06 19:45:00'),
    (12, 1, '2025-09-06 17:05:00', '2025-09-06 19:55:00'),
    (13, 1, '2025-09-06 17:20:00', '2025-09-06 19:50:00'),
    (14, 1, '2025-09-06 17:30:00', '2025-09-06 19:40:00'),
    (15, 1, '2025-09-06 17:10:00', '2025-09-06 19:30:00'),
    (16, 1, '2025-09-06 17:25:00', '2025-09-06 19:55:00'),
    (17, 1, '2025-09-06 17:18:00', '2025-09-06 19:35:00'),
    (18, 1, '2025-09-06 17:35:00', '2025-09-06 20:00:00'),
    (19, 1, '2025-09-06 17:12:00', '2025-09-06 19:42:00'),
    (20, 1, '2025-09-06 17:22:00', '2025-09-06 19:48:00'),
    (21, 1, '2025-09-06 17:28:00', '2025-09-06 19:52:00'),
    (26, 1, '2025-09-06 17:40:00', '2025-09-06 19:25:00'),
    (27, 1, '2025-09-06 17:33:00', '2025-09-06 19:38:00'),
    (28, 1, '2025-09-06 17:45:00', '2025-09-06 19:30:00');

-- Parent Info Night
INSERT INTO Attendance (personId, eventId, checkedInAt, checkedOutAt) VALUES
    (41, 2, '2025-09-12 18:55:00', '2025-09-12 20:50:00'),
    (42, 2, '2025-09-12 18:55:00', '2025-09-12 20:50:00'),
    (43, 2, '2025-09-12 19:02:00', '2025-09-12 20:55:00'),
    (44, 2, '2025-09-12 19:02:00', '2025-09-12 20:55:00'),
    (45, 2, '2025-09-12 19:10:00', '2025-09-12 20:45:00'),
    (47, 2, '2025-09-12 19:05:00', '2025-09-12 20:48:00');

-- Worship Night
INSERT INTO Attendance (personId, eventId, checkedInAt, checkedOutAt) VALUES
    (11, 3, '2025-09-20 19:05:00', '2025-09-20 21:25:00'),
    (13, 3, '2025-09-20 19:10:00', '2025-09-20 21:30:00'),
    (15, 3, '2025-09-20 19:03:00', '2025-09-20 21:20:00'),
    (17, 3, '2025-09-20 19:12:00', '2025-09-20 21:28:00'),
    (19, 3, '2025-09-20 19:08:00', '2025-09-20 21:22:00'),
    (21, 3, '2025-09-20 19:15:00', '2025-09-20 21:30:00'),
    (23, 3, '2025-09-20 19:07:00', '2025-09-20 21:18:00'),
    (12, 3, '2025-09-20 19:20:00', '2025-09-20 21:15:00'),
    (14, 3, '2025-09-20 19:18:00', '2025-09-20 21:25:00');

-- Fall Retreat - Multi-day event
INSERT INTO Attendance (personId, eventId, checkedInAt, checkedOutAt) VALUES
    (11, 6, '2025-10-18 15:10:00', '2025-10-20 13:45:00'),
    (12, 6, '2025-10-18 15:05:00', '2025-10-20 13:50:00'),
    (13, 6, '2025-10-18 15:20:00', '2025-10-20 13:40:00'),
    (14, 6, '2025-10-18 15:15:00', '2025-10-20 13:55:00'),
    (15, 6, '2025-10-18 15:25:00', '2025-10-20 13:35:00'),
    (16, 6, '2025-10-18 15:18:00', '2025-10-20 13:48:00'),
    (17, 6, '2025-10-18 15:12:00', '2025-10-20 13:52:00'),
    (18, 6, '2025-10-18 15:30:00', '2025-10-20 13:30:00'),
    (19, 6, '2025-10-18 15:22:00', '2025-10-20 13:42:00'),
    (20, 6, '2025-10-18 15:28:00', '2025-10-20 13:38:00'),
    (21, 6, '2025-10-18 15:08:00', '2025-10-20 13:58:00'),
    (22, 6, '2025-10-18 15:35:00', '2025-10-20 14:00:00'),
    (26, 6, '2025-10-18 15:40:00', '2025-10-20 13:25:00'),
    (27, 6, '2025-10-18 15:32:00', '2025-10-20 13:44:00');

-- Thanksgiving Dinner - Currently checked in (event is tomorrow from Nov 23 perspective)
-- Note: This is future data from Nov 23 perspective, so left blank for realism

-- ============================================================================
-- SMALL GROUP MEETING ATTENDANCE
-- ============================================================================

-- High School Boys meeting attendance (Group 1, multiple meetings)
-- Meeting 1 (Sept 9)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (1, 12, '2025-09-09 19:02:00', '2025-09-09 20:28:00'),
    (1, 14, '2025-09-09 19:05:00', '2025-09-09 20:30:00'),
    (1, 16, '2025-09-09 19:00:00', '2025-09-09 20:25:00'),
    (1, 18, '2025-09-09 19:10:00', '2025-09-09 20:32:00'),
    (1, 20, '2025-09-09 19:08:00', '2025-09-09 20:20:00'),
    (1, 22, '2025-09-09 19:03:00', '2025-09-09 20:30:00');

-- Meeting 5 (Oct 7)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (5, 12, '2025-10-07 19:05:00', '2025-10-07 20:35:00'),
    (5, 14, '2025-10-07 19:02:00', '2025-10-07 20:30:00'),
    (5, 16, '2025-10-07 19:08:00', '2025-10-07 20:32:00'),
    (5, 18, '2025-10-07 19:00:00', '2025-10-07 20:28:00'),
    (5, 20, '2025-10-07 19:12:00', '2025-10-07 20:40:00'),
    (5, 22, '2025-10-07 19:03:00', '2025-10-07 20:33:00'),
    (5, 24, '2025-10-07 19:15:00', '2025-10-07 20:35:00');

-- Meeting 11 (Nov 18) - Most recent
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (11, 12, '2025-11-18 19:03:00', '2025-11-18 20:42:00'),
    (11, 14, '2025-11-18 19:00:00', '2025-11-18 20:38:00'),
    (11, 16, '2025-11-18 19:10:00', '2025-11-18 20:40:00'),
    (11, 18, '2025-11-18 19:05:00', '2025-11-18 20:45:00'),
    (11, 22, '2025-11-18 19:08:00', '2025-11-18 20:35:00'),
    (11, 24, '2025-11-18 19:02:00', '2025-11-18 20:40:00');

-- High School Girls meeting attendance (Group 2)
-- Meeting 1 (Sept 10)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (12, 11, '2025-09-10 19:05:00', '2025-09-10 20:35:00'),
    (12, 13, '2025-09-10 19:02:00', '2025-09-10 20:32:00'),
    (12, 15, '2025-09-10 19:00:00', '2025-09-10 20:30:00'),
    (12, 17, '2025-09-10 19:08:00', '2025-09-10 20:38:00'),
    (12, 19, '2025-09-10 19:10:00', '2025-09-10 20:40:00'),
    (12, 21, '2025-09-10 19:12:00', '2025-09-10 20:35:00'),
    (12, 23, '2025-09-10 19:03:00', '2025-09-10 20:33:00');

-- Meeting 11 (Nov 19)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (22, 11, '2025-11-19 19:00:00', '2025-11-19 20:45:00'),
    (22, 13, '2025-11-19 19:05:00', '2025-11-19 20:42:00'),
    (22, 15, '2025-11-19 19:03:00', '2025-11-19 20:40:00'),
    (22, 17, '2025-11-19 19:10:00', '2025-11-19 20:48:00'),
    (22, 19, '2025-11-19 19:08:00', '2025-11-19 20:38:00'),
    (22, 21, '2025-11-19 19:12:00', '2025-11-19 20:50:00'),
    (22, 23, '2025-11-19 19:02:00', '2025-11-19 20:43:00'),
    (22, 25, '2025-11-19 19:15:00', '2025-11-19 20:35:00');

-- Middle School Boys meeting attendance (Group 3)
-- Meeting 1 (Sept 11)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (23, 26, '2025-09-11 18:32:00', '2025-09-11 19:55:00'),
    (23, 28, '2025-09-11 18:35:00', '2025-09-11 19:58:00'),
    (23, 30, '2025-09-11 18:30:00', '2025-09-11 19:52:00'),
    (23, 32, '2025-09-11 18:40:00', '2025-09-11 20:00:00'),
    (23, 34, '2025-09-11 18:38:00', '2025-09-11 19:50:00');

-- Meeting 11 (Nov 20)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (33, 26, '2025-11-20 18:30:00', '2025-11-20 20:15:00'),
    (33, 28, '2025-11-20 18:35:00', '2025-11-20 20:10:00'),
    (33, 30, '2025-11-20 18:32:00', '2025-11-20 20:12:00'),
    (33, 32, '2025-11-20 18:40:00', '2025-11-20 20:05:00'),
    (33, 34, '2025-11-20 18:28:00', '2025-11-20 20:18:00'),
    (33, 36, '2025-11-20 18:45:00', '2025-11-20 20:00:00');

-- Middle School Girls meeting attendance (Group 4)
-- Meeting 1 (Sept 11)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (34, 27, '2025-09-11 18:32:00', '2025-09-11 20:05:00'),
    (34, 29, '2025-09-11 18:30:00', '2025-09-11 20:00:00'),
    (34, 31, '2025-09-11 18:35:00', '2025-09-11 20:08:00'),
    (34, 33, '2025-09-11 18:40:00', '2025-09-11 20:02:00'),
    (34, 35, '2025-09-11 18:33:00', '2025-09-11 20:10:00');

-- Meeting 11 (Nov 20)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (44, 27, '2025-11-20 18:30:00', '2025-11-20 20:20:00'),
    (44, 29, '2025-11-20 18:35:00', '2025-11-20 20:15:00'),
    (44, 31, '2025-11-20 18:32:00', '2025-11-20 20:18:00'),
    (44, 33, '2025-11-20 18:38:00', '2025-11-20 20:12:00'),
    (44, 35, '2025-11-20 18:28:00', '2025-11-20 20:25:00'),
    (44, 37, '2025-11-20 18:40:00', '2025-11-20 20:10:00'),
    (44, 39, '2025-11-20 18:45:00', '2025-11-20 20:08:00');

-- Freshmen Connect meeting attendance (Group 5)
-- Meeting 1 (Sept 7)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (45, 11, '2025-09-07 18:02:00', '2025-09-07 19:25:00'),
    (45, 12, '2025-09-07 18:00:00', '2025-09-07 19:28:00'),
    (45, 13, '2025-09-07 18:05:00', '2025-09-07 19:22:00'),
    (45, 14, '2025-09-07 18:03:00', '2025-09-07 19:30:00');

-- Meeting 11 (Nov 16)
INSERT INTO SmallGroupMeetingAttendance (groupMeetingId, personId, checkedInAt, checkedOutAt) VALUES
    (55, 11, '2025-11-16 18:00:00', '2025-11-16 19:40:00'),
    (55, 12, '2025-11-16 18:02:00', '2025-11-16 19:38:00'),
    (55, 13, '2025-11-16 18:05:00', '2025-11-16 19:42:00'),
    (55, 14, '2025-11-16 18:03:00', '2025-11-16 19:35:00'),
    (55, 15, '2025-11-16 18:10:00', '2025-11-16 19:45:00');

-- ============================================================================
-- END OF SAMPLE DATA
-- ============================================================================

-- Verify data was inserted
SELECT COUNT(*) AS TotalPeople FROM Person;
SELECT COUNT(*) AS TotalStudents FROM PersonRole WHERE roleId = 1;
SELECT COUNT(*) AS TotalEvents FROM Event;
SELECT COUNT(*) AS TotalSmallGroups FROM SmallGroup;
SELECT COUNT(*) AS TotalMeetings FROM SmallGroupMeeting;