import sqlite3

connection = sqlite3.connect('song_user2.db')

crsr = connection.cursor()

# # SQL command to insert the data in the table
def insert_user_emotion(user_id):
   sql_command = """INSERT INTO user_emotion (id) VALUES (?);"""
   crsr.execute(sql_command,(user_id,))
   connection.commit()

def insert_song_table(song_name,artist_name):
   sql_command = """INSERT INTO song_table (song_name,artist_name) VALUES (?,?);"""
   crsr.execute(sql_command,(song_name,artist_name))
   connection.commit()

def insert_song_user_rating(user_id,songN,rating):
   sql_command = """SELECT id FROM song_table WHERE song_name=?;"""
   abc = crsr.execute(sql_command,(songN,))
   for row in abc:
      songId = row[0]
   sql_command = """INSERT INTO song_user_rating VALUES (?,?,?,1);"""
   crsr.execute(sql_command,(user_id,songId,rating))
   connection.commit()

def update_song_user_rating(user_id,songN,rating):
   sql_command = """SELECT id FROM song_table WHERE song_name=?;"""
   abc = crsr.execute(sql_command, (songN,))
   for row in abc:
      songId = row[0]
   sql_command = """SELECT rating,play_count FROM song_user_rating WHERE user_id=? AND song_id=?;"""
   bcd = crsr.execute(sql_command, (user_id,songId))
   for row2 in bcd:
      rate = int(row2[0])
      play_count = int(row2[1])
   new_rate = (rate*play_count+int(rating))/(play_count+1)
   sql_command = """UPDATE song_user_rating SET rating = ?,play_count=play_count+1 WHERE user_id=? AND song_id=?;"""
   crsr.execute(sql_command,(new_rate,user_id,songId))
   connection.commit()


def display(table_name):
   sql_comm = """SELECT * FROM """+table_name+';'
   cursor = crsr.execute(sql_comm)
   for row in cursor:
      print(row)
# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
