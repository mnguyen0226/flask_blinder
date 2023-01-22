import mysql.connector

# connect to local database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password123",
    auth_plugin="mysql_native_password",
)

# object interact with database
my_cursor = mydb.cursor()

# create new database
my_cursor.execute("CREATE DATABASE flask_y")

# show all database
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
