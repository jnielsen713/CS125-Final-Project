# How to start the app
1. Clone the repository on to your device, and install all packages listed in requirements.txt
2. Start a docker container, be sure to note your user information
3. Within the docker container:
   -- copy over youth_group_schema.sql and youth_group_data.sql files
   -- run youth_group_schema.sql, and then youth_group_data.sql (the data file should print data verification information in the form of query results)
4. In your IDE of choice, create a copy of template.env and rename it to just .env
5. Add in your user information! .gitignore will keep this private to your device.
6. Run db_programming.py, and it will spin up!
7. Use docker or the terminal to see where the app is running, and you can use Insomnia to read data by pasting the link and following it with /people, /events, /smallgroups, etc. (endpoints can be found in db_programming.py)
8. DOCKER COMMANDS for steps 2/3:
   -- Navigate to the directory containing your Dockerfile
   -- docker build -t mysql-cs125 .
   -- docker run --name mysql-cs125 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=cs125 -d mysql-cs125
   -- Load schema: docker exec -i mysql-cs125 mysql -u root -pcs125 < youth_group_schema.sql
   -- Load data: docker exec -i mysql-cs125 mysql -u root -pcs125 < youth_group_data.sql
9. To use the frontend, open index.html AFTER running db_programming.py
   
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
