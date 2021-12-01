import sqlite3

connection = sqlite3.connect('song_user2.db')

crsr = connection.cursor()

# print statement will execute if there
# are no errors
print("Connected to the database")

# SQL command to create a table in the database
# sql_command = """CREATE TABLE song_user_rating (
# user_id VARCHAR(20) PRIMARY KEY,
# song_id VARCHAR(20),
# rating INT);"""
# crsr.execute(sql_command)


# # SQL command to insert the data in the table
def insert(user_id,song_id,rating):
   sql_command = """INSERT INTO song_user_rating VALUES (?,?,?);"""
   crsr.execute(sql_command,(user_id,song_id,rating))

def display():
   cursor = crsr.execute("SELECT * FROM song_user_rating")
   for row in cursor:
      print(row)
# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()


