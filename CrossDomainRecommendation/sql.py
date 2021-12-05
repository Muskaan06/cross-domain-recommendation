import sqlite3

connection = sqlite3.connect('SongUser.db')

crsr = connection.cursor()


# # SQL command to insert the data in the table
def insert_user_emotion(user_id):
    sql_command = """INSERT INTO user_emotion (id) VALUES (?);"""
    crsr.execute(sql_command, (user_id,))
    connection.commit()


def update_user_emotion(user_id, emo_list, rating):
    # denominator for wt. avg
    sql_command2 = """SELECT SUM(rating*play_count) FROM song_user_rating WHERE user_id=?; """
    demo = crsr.execute(sql_command2, (user_id,))
    # emo_user = [0,0,0,0,0,0,0,0,0,0]
    for row1 in demo:
        denom = row1[0]

    sql_command1 = """SELECT Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust FROM user_emotion WHERE id=?;"""
    demo2 = crsr.execute(sql_command1, (user_id,))
    for row2 in demo2:
        emo_user = list(row2)

    for i, emo in enumerate(emo_user):
        emo_user[i] = (emo * denom + emo_list[i] * rating) / (denom + rating)
    print("--------------------------")
    print(emo_user)

    sql_command = """UPDATE user_emotion SET Positive=?, Negative=?, Anger=?, Anticipation=?, Disgust=?, Fear=?, Joy=?, Sadness=?, Surprise=?, Trust=? WHERE id=?;"""
    crsr.execute(sql_command, (
        emo_user[0], emo_user[1], emo_user[2], emo_user[3], emo_user[4], emo_user[5], emo_user[6], emo_user[7],
        emo_user[8],
        emo_user[9], user_id))

    connection.commit()


def get_song_emotion(song_id):
    sql_command1 = """SELECT Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust FROM song_emotion WHERE song_id=?;"""
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


def get_song_id(songN):
    sql_command = """SELECT id FROM song_table WHERE song_name=?;"""
    abc = crsr.execute(sql_command, (songN,))
    for row in abc:
        songId = row[0]
    return songId


def get_user_ratings(userID):
    sql_command = """SELECT song_id,rating FROM song_user_rating WHERE user_id=?;"""
    abc = crsr.execute(sql_command, (userID,))
    user_ratings = []
    for row in abc:
        user_ratings.append(list(row))
    return user_ratings

def get_user_emotion(userID):
    sql_command1 = """SELECT Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust FROM user_emotion WHERE id=?;"""
    demo2 = crsr.execute(sql_command1, (userID,))
    for row2 in demo2:
        return list(row2)

def insert_song_table(song_name, artist_name):
    sql_command = """INSERT INTO song_table (song_name,artist_name) VALUES (?,?);"""
    crsr.execute(sql_command, (song_name, artist_name))
    connection.commit()


def insert_song_user_rating(user_id, songN, rating):
    sql_command = """SELECT id FROM song_table WHERE song_name=?;"""
    abc = crsr.execute(sql_command, (songN,))
    for row in abc:
        songId = row[0]
    sql_command = """INSERT INTO song_user_rating VALUES (?,?,?,1);"""
    crsr.execute(sql_command, (user_id, songId, rating))
    connection.commit()


def update_song_user_rating(user_id, songN, rating):
    sql_command = """SELECT id FROM song_table WHERE song_name=?;"""
    abc = crsr.execute(sql_command, (songN,))
    for row in abc:
        songId = row[0]
    sql_command = """SELECT rating,play_count FROM song_user_rating WHERE user_id=? AND song_id=?;"""
    bcd = crsr.execute(sql_command, (user_id, songId))
    rate = 0
    play_count = 0
    for row2 in bcd:
        rate = float(row2[0])
        play_count = float(row2[1])
    new_rate = (rate * play_count + float(rating)) / (play_count + 1)
    sql_command = """UPDATE song_user_rating SET rating = ?,play_count=play_count+1 WHERE user_id=? AND song_id=?;"""
    crsr.execute(sql_command, (new_rate, user_id, songId))
    connection.commit()


def insert_song_emotion(songN, emo_lis):
    sql_command = """SELECT id FROM song_table WHERE song_name=?;"""
    abc = crsr.execute(sql_command, (songN,))
    for row in abc:
        songId = row[0]
    sql_command = """INSERT INTO song_emotion VALUES (?,?,?,?,?,?,?,?,?,?,?);"""
    crsr.execute(sql_command, (
        songId, emo_lis[0], emo_lis[1], emo_lis[2], emo_lis[3], emo_lis[4], emo_lis[5], emo_lis[6], emo_lis[7],
        emo_lis[8],
        emo_lis[9]))
    connection.commit()


def display(table_name):
    sql_comm = """SELECT * FROM """ + table_name + ';'
    cursor = crsr.execute(sql_comm)
    for row in cursor:
        print(row)


def display_song_rec(rec_id):
    sql_command = """SELECT song_name,artist_name FROM song_table WHERE id=?;"""
    cursor = crsr.execute(sql_command, (rec_id,))
    for row in cursor:
        print(row)
        return row[0]

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
