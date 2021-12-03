import sqlite3

connection = sqlite3.connect('song_user2.db')

crsr = connection.cursor()

# print statement will execute if there
# are no errors
print("Connected to the database")

sql_command = """CREATE TABLE user_emotion (
id              VARCHAR(50) ,
Positive        FLOAT DEFAULT '0.00',
Negative        FLOAT DEFAULT '0.00',
Anger           FLOAT DEFAULT '0.00',
Anticipation    FLOAT DEFAULT '0.00',
Disgust         FLOAT DEFAULT '0.00',
Fear            FLOAT DEFAULT '0.00',
Joy             FLOAT DEFAULT '0.00',
Sadness         FLOAT DEFAULT '0.00',
Surprise        FLOAT DEFAULT '0.00',
Trust           FLOAT DEFAULT '0.00',
PRIMARY KEY (id));"""
crsr.execute(sql_command)


sql_command = """CREATE TABLE song_table (
id              INTEGER PRIMARY KEY AUTOINCREMENT,
song_name       VARCHAR(50),
artist_name     VARCHAR(20),
UNIQUE (song_name,artist_name));"""
crsr.execute(sql_command)


sql_command = """CREATE TABLE song_user_rating (
user_id         VARCHAR(50),
song_id         VARCHAR(20),
rating          INT NOT NULL,
play_count      INT NOT NULL,
FOREIGN KEY (user_id) REFERENCES user_emotion(id),
FOREIGN KEY (song_id) REFERENCES song_table(id),
PRIMARY KEY (user_id,song_id));"""
crsr.execute(sql_command)



sql_command = """CREATE TABLE song_emotion (
song_id         INT ,
Positive        FLOAT DEFAULT 0.0,
Negative        FLOAT DEFAULT 0.0,
Anger           FLOAT DEFAULT 0.0,
Anticipation    FLOAT DEFAULT 0.0,
Disgust         FLOAT DEFAULT 0.0,
Fear            FLOAT DEFAULT 0.0,
Joy             FLOAT DEFAULT 0.0,
Sadness         FLOAT DEFAULT 0.0,
Surprise        FLOAT DEFAULT 0.0,
Trust           FLOAT DEFAULT 0.0,
FOREIGN KEY (song_id) REFERENCES song_table(id),
PRIMARY KEY (song_id));"""
crsr.execute(sql_command)

connection.commit()

connection.close()