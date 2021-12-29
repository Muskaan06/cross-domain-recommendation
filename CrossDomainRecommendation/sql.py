
DB_HOST = 'songuser-db.cwvddet8zv5c.us-east-1.rds.amazonaws.com'
DB_NAME = 'SongUser'
DB_USER = 'postgres'
DB_PASS = 'C3LOKOr9xXgGxs22x3dO'

import psycopg2
import genre

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432, sslmode='require')


crsr = connection.cursor()

# TODO: change all select executions to crsr.fetchall() like done in fetch_song_genres()
with connection:
    # # SQL command to insert the data in the table
    def insert_user_emotion(user_id):
        sql_command = """INSERT INTO user_emotion (id) VALUES (%s);"""
        crsr.execute(sql_command, (user_id,))
        connection.commit()


    def update_user_emotion(user_id, emo_list, rating):
        # denominator for wt. avg
        sql_command2 = """SELECT SUM(rating*play_count) FROM song_user_rating WHERE user_id=%s; """
        demo = crsr.execute(sql_command2, (user_id,))
        # emo_user = [0,0,0,0,0,0,0,0,0,0]
        for row1 in demo:
            denom = row1[0]

        sql_command1 = """SELECT Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust FROM user_emotion WHERE id=%s;"""
        demo2 = crsr.execute(sql_command1, (user_id,))
        for row2 in demo2:
            emo_user = list(row2)

        for i, emo in enumerate(emo_user):
            emo_user[i] = (emo * denom + emo_list[i] * rating) / (denom + rating)
        print("--------------------------")
        # print(emo_user)

        sql_command = """UPDATE user_emotion SET Positive=%s, Negative=%s, Anger=%s, Anticipation=%s, Disgust=%s, Fear=%s, Joy=%s, Sadness=%s, Surprise=%s, Trust=%s WHERE id=%s;"""
        crsr.execute(sql_command, (
            emo_user[0], emo_user[1], emo_user[2], emo_user[3], emo_user[4], emo_user[5], emo_user[6], emo_user[7],
            emo_user[8],
            emo_user[9], user_id))

        connection.commit()


    def update_song_genre(songN, artist):
        tags = genre.get_genre(songN, artist)
        print(tags)
        result = ','.join(tag for tag in tags)
        song_id = get_song_id_input(songN, artist)
        sql_command = '''UPDATE song_emotion
                         SET Tags=%s
                         WHERE song_id=%s'''
        crsr.execute(sql_command, (result, song_id))
        connection.commit()

    def fetch_song_genres():
        sql_command = """SELECT song_id FROM song_emotion"""
        # demo2 = crsr.execute(sql_command)
        # song_list = []
        #
        # for row2 in demo2:
        #     song_list.append((row2[0]))
        crsr.execute(sql_command)
        song_list = crsr.fetchall()
        song_list = [song[0] for song in song_list]

        # song_genre = []
        sql_command = """SELECT Tags FROM song_emotion"""
        # demo2 = crsr.execute(sql_command)
        # for row2 in demo2:
        #     song_genre.append(list(row2))
        crsr.execute(sql_command)
        song_genre = crsr.fetchall()
        song_genre = [gen[0] for gen in song_genre]
        song_genre = [gen.split(",") for gen in song_genre]

        return song_genre, song_list

    def get_song_emotion(song_id):
        sql_command1 = """SELECT Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust FROM song_emotion WHERE song_id=%s;"""
        demo2 = crsr.execute(sql_command1, (song_id,))
        for row2 in demo2:
            return list(row2)


    def fetch_song_emotion():
        sql_command = """SELECT song_id FROM song_emotion"""
        demo2 = crsr.execute(sql_command)
        song_list = []

        for row2 in demo2:
            song_list.append((row2[0]))

        song_emo = []
        sql_command = """SELECT Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust FROM song_emotion"""
        demo2 = crsr.execute(sql_command)
        for row2 in demo2:
            song_emo.append(list(row2))

        return song_emo, song_list


    def fetch_user_emotion():
        sql_command = """SELECT id FROM user_emotion"""
        demo2 = crsr.execute(sql_command)
        user_list = []

        for row2 in demo2:
            user_list.append((row2[0]))

        user_emo = []
        sql_command = """SELECT Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust 
                         FROM user_emotion"""
        demo2 = crsr.execute(sql_command)
        for row2 in demo2:
            user_emo.append(list(row2))

        return user_emo, user_list


    def get_song_id(songN):
        sql_command = """SELECT id FROM song_table WHERE song_name=%s;"""
        abc = crsr.execute(sql_command, (songN,))
        songId = 0
        for row in abc:
            songId = row[0]
        return songId


    def get_user_ratings(userID):
        sql_command = """SELECT song_id,rating FROM song_user_rating WHERE user_id=%s;"""
        abc = crsr.execute(sql_command, (userID,))
        user_ratings = []
        for row in abc:
            user_ratings.append(list(row))
        return user_ratings


    def get_user_emotion(userID):
        sql_command1 = """SELECT Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust FROM user_emotion WHERE id=%s;"""
        demo2 = crsr.execute(sql_command1, (userID,))
        for row2 in demo2:
            return list(row2)


    def get_song_id_input(song_name, artist_name):
        sql_command1 = """SELECT id FROM song_table WHERE song_name=%s and artist_name=%s;"""
        qwe = crsr.execute(sql_command1, (song_name, artist_name,))
        song_id_input = 0
        for row in qwe:
            song_id_input = row[0]
        return song_id_input


    def get_user_list_common(song_id_input):
        sql_command2 = """SELECT user_id FROM song_user_rating WHERE song_id=%s;"""
        abc = crsr.execute(sql_command2, (song_id_input,))
        user_list_common = []
        for row in abc:
            user_list_common.append(row[0])
        return user_list_common


    def get_user_song_matrix(user_list_common):
        user_song_matrix = []
        for users in user_list_common:

            sql_command3 = """SELECT song_id from song_user_rating where user_id=%s;"""
            efg = crsr.execute(sql_command3, (users,))
            for row in efg:
                user_song_matrix.append(row[0])
        return user_song_matrix


    def print_cf_output(int_list):
        sql_command4 = """SELECT song_name,artist_name FROM song_table WHERE id in """ + int_list + ';'
        sdf = crsr.execute(sql_command4)

        for row in sdf:
            print(row[0], " by ", row[1])


    def insert_song_table(song_name, artist_name):
        sql_command = """INSERT INTO song_table (song_name,artist_name) VALUES (%s,%s);"""
        crsr.execute(sql_command, (song_name, artist_name))
        connection.commit()


    def insert_song_user_rating(user_id, songN, rating):
        sql_command = """SELECT id FROM song_table WHERE song_name=%s;"""
        abc = crsr.execute(sql_command, (songN,))
        songId = 0
        for row in abc:
            songId = row[0]
        sql_command = """INSERT INTO song_user_rating VALUES (%s,%s,%s,1);"""
        crsr.execute(sql_command, (user_id, songId, rating))
        connection.commit()


    def update_song_user_rating(user_id, songN, rating):
        sql_command = """SELECT id FROM song_table WHERE song_name=%s;"""
        abc = crsr.execute(sql_command, (songN,))
        songId = 0
        for row in abc:
            songId = row[0]
        sql_command = """SELECT rating,play_count FROM song_user_rating WHERE user_id=%s AND song_id=%s;"""
        bcd = crsr.execute(sql_command, (user_id, songId))
        rate = 0
        play_count = 0
        for row2 in bcd:
            rate = float(row2[0])
            play_count = float(row2[1])
        new_rate = (rate * play_count + float(rating)) / (play_count + 1)
        sql_command = """UPDATE song_user_rating SET rating = %s,play_count=play_count+1 WHERE user_id=%s AND song_id=%s;"""
        crsr.execute(sql_command, (new_rate, user_id, songId))
        connection.commit()


    def insert_song_emotion(songN, artist, emo_lis):

        sql_command = """SELECT id FROM song_table WHERE song_name=%s AND artist_name=%s;"""
        crsr.execute("ROLLBACK")
        crsr.execute(sql_command, (songN, artist))
        songId = 0
        abc = crsr.fetchall()
        for row in abc:
            songId = row[0]
        print('SONG_ID----->',songId)
        tags = genre.get_genre(songN, artist)
        result = ','.join(tag for tag in tags)
        sql_command = """INSERT INTO song_emotion VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        crsr.execute(sql_command, (
            songId, emo_lis[0], emo_lis[1], emo_lis[2], emo_lis[3], emo_lis[4], emo_lis[5], emo_lis[6], emo_lis[7],
            emo_lis[8], emo_lis[9], result))
        connection.commit()


    def display(table_name):
        sql_comm = """SELECT * FROM """ + table_name + ';'
        cursor = crsr.execute(sql_comm)
        for row in cursor:
            print(row)


    def get_song_table():
        sql_comm = '''SELECT * FROM song_table'''
        output = crsr.execute(sql_comm)
        return output


    def display_song_rec(rec_id):
        sql_command = """SELECT song_name,artist_name FROM song_table WHERE id=%s;"""
        cursor = crsr.execute(sql_command, (rec_id,))
        for row in cursor:
            print(row)
            return row[0]

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.

