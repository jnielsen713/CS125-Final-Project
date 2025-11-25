# How to start the app
1. Clone the repository on to your device, and install packages mysql-connector-python, python-dotenv, and Flask
2. Start a docker container, be sure to note your user information
3. Within the docker container:
   -- copy over youth_group_schema.sql and youth_group_data.sql files
   -- run youth_group_schema.sql, and then youth_group_data.sql (the data file should print data verification information in the form of query results)
4. In your IDE of choice, create a copy of template.env and rename it to just .env
5. Add in your user information! .gitignore will keep this private to your device.
6. Run db_programming.py, and it will spin up!
7. Use docker or the terminal to see where the app is running, and you can use Insomnia to read data by pasting the link and following it with /people, /events, or /smallgroups. More to be added in the future. 
   
# FAQ
**1. What's your team name?**

Student T JOIN Student J

**2. Who is using this?**

Youth group leaders/organizers who manage the data for events, students, etc. 

**3. What do they want to do?**

They want to keep track of everyone with stake in the Youth group, (Parents, Students, Leaders, Volunteers, etc.).

They want to track event details and attendance.

They want to record summaries of what happened during each event

They want real-time check-in visibility so they can know exactly what is happening at any given time.

**4. What should (or shouldn't) they be able to do?**

*Should:*

The things listed above

*Shouldn't:*

Modify data for any person outside the scope of an event if they're not in charge
Change assignments of volunteers without their knowledge
Explode, etc.
