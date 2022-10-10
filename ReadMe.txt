The web application serves as a tool for browsing employee records. The records include basic information about the employees which includes their address, email, role, contact details and the date they joined the company. The database contains two tables. One table is used to store information about the employees who have a contract of employment with the company and the second table contains information about the employees who do not have a contract or are temporary workers. Two types of users exist: regular and admin. Both users need to register before login. The basic users can browse the records, read, add records and edit employee information. The admin user has the same permissions as the regular users in addition to being able to delete records.

Flask has been used as the framework for developing the web application in the python language. SQLAlchemy is the SQL toolkit used to gain easy access to and interact with the SQLite database. 

To run the app, activate the virtual environement:

macOS: 
 $python3 -m venv. venv
 $source .venv/bin/activate

To run the app:
 $flask run
 
 