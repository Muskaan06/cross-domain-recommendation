import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432, sslmode='require')

with conn:
    crsr = conn.cursor()

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
    print("Table created!")

    sql_command = """CREATE TABLE song_table (
    id              SERIAL PRIMARY KEY,
    song_name       VARCHAR(50),
    artist_name     VARCHAR(20),
    UNIQUE (song_name,artist_name));"""
    crsr.execute(sql_command)
    print("Table created!")

    sql_command = """CREATE TABLE song_user_rating (
    user_id         VARCHAR(50),
    song_id         INT NOT NULL,
    rating          FLOAT NOT NULL,
    play_count      INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_emotion(id),
    FOREIGN KEY (song_id) REFERENCES song_table(id),
    PRIMARY KEY (user_id,song_id));"""
    crsr.execute(sql_command)
    print("Table created!")

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
    Tags            VARCHAR(200) DEFAULT '',
    FOREIGN KEY (song_id) REFERENCES song_table(id),
    PRIMARY KEY (song_id));"""
    crsr.execute(sql_command)
    print("Table created!")

    conn.commit()

    # sql_comm = """DROP TABLE song_emotion;"""
    # crsr.execute(sql_comm)
    # conn.commit()
