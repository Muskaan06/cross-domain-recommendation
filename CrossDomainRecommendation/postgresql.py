DB_HOST = 'songuser-db.cwvddet8zv5c.us-east-1.rds.amazonaws.com'
DB_NAME = 'SongUser'
DB_USER = 'postgres'
DB_PASS = 'C3LOKOr9xXgGxs22x3dO'

import psycopg2

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432, sslmode='require')

with conn:
    crsr = conn.cursor()

    # sql_command = """CREATE TABLE song_table (
    # id              SERIAL PRIMARY KEY,
    # song_name       VARCHAR(50),
    # artist_name     VARCHAR(20),
    # UNIQUE (song_name,artist_name));"""
    # crsr.execute(sql_command)

    sql_command = """INSERT INTO song_table(song_name,artist_name) VALUES (%s,%s);"""
    crsr.execute(sql_command, ('perfect', 'ed sheeran'))
    conn.commit()

    sql_disp = '''SELECT * FROM song_table'''
    crsr.execute(sql_disp)

    print(crsr.fetchall())
