# script to create a MySQL database
import mysql.connector

# connect and get db object
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password123",
    auth_plugin="mysql_native_password",
)

# object interact with local db
my_cursor = mydb.cursor()

# note: "users" is the name of db initialize in main.py (app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:password123@localhost/our_users"). Uncomment to create a db again
# my_cursor.execute("CREATE DATABASE our_users2")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)

# to create a mysql db, we have to run "python create_db.py"
