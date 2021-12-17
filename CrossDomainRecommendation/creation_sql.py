import sqlite3

connection = sqlite3.connect('SongUser.db')

crsr = connection.cursor()

#CREATING TABLES
# # print statement will execute if there
# # are no errors
# print("Connected to the database")
#
# sql_command = """CREATE TABLE user_emotion (
# id              VARCHAR(50) ,
# Positive        FLOAT DEFAULT '0.00',
# Negative        FLOAT DEFAULT '0.00',
# Anger           FLOAT DEFAULT '0.00',
# Anticipation    FLOAT DEFAULT '0.00',
# Disgust         FLOAT DEFAULT '0.00',
# Fear            FLOAT DEFAULT '0.00',
# Joy             FLOAT DEFAULT '0.00',
# Sadness         FLOAT DEFAULT '0.00',
# Surprise        FLOAT DEFAULT '0.00',
# Trust           FLOAT DEFAULT '0.00',
# PRIMARY KEY (id));"""
# crsr.execute(sql_command)
#
#
# sql_command = """CREATE TABLE song_table (
# id              id SERIAL PRIMARY KEY,
# song_name       VARCHAR(50),
# artist_name     VARCHAR(20),
# UNIQUE (song_name,artist_name));"""
# crsr.execute(sql_command)
#
#
# sql_command = """CREATE TABLE song_user_rating (
# user_id         VARCHAR(50),
# song_id         VARCHAR(20),
# rating          FLOAT NOT NULL,
# play_count      NUMERIC NOT NULL,
# FOREIGN KEY (user_id) REFERENCES user_emotion(id),
# FOREIGN KEY (song_id) REFERENCES song_table(id),
# PRIMARY KEY (user_id,song_id));"""
# crsr.execute(sql_command)
#
#
#
# sql_command = """CREATE TABLE song_emotion (
# song_id         NUMERIC ,
# Positive        FLOAT DEFAULT 0.0,
# Negative        FLOAT DEFAULT 0.0,
# Anger           FLOAT DEFAULT 0.0,
# Anticipation    FLOAT DEFAULT 0.0,
# Disgust         FLOAT DEFAULT 0.0,
# Fear            FLOAT DEFAULT 0.0,
# Joy             FLOAT DEFAULT 0.0,
# Sadness         FLOAT DEFAULT 0.0,
# Surprise        FLOAT DEFAULT 0.0,
# Trust           FLOAT DEFAULT 0.0,
# FOREIGN KEY (song_id) REFERENCES song_table(id),
# PRIMARY KEY (song_id));"""
# crsr.execute(sql_command)
#
#
#

#ADDED SONG TAGS
# sql_command = """ALTER TABLE song_emotion ADD Tags VARCHAR(200) DEFAULT '';"""
# crsr.execute(sql_command)
# connection.commit()

connection.close()
