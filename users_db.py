import sqlite3 as sql

con = sql.connect('db_users.db')

curs = con.cursor()
curs.execute("DROP TABLE IF EXISTS users")

#Create users table 
sql ='''CREATE TABLE "users" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"NAME"	TEXT,
	"EMAIL"	TEXT,
    "is_admin" BOOLEAN,
    "PASS" TEXT
)'''

curs.execute(sql)

con.commit()

con.close()