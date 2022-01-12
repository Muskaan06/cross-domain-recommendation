import sql
import input_model
import lyrics
import sqlite3

from CrossDomainRecommendation import genre
from emotion_score import text_emotion
import re
from clustering import song_rec
import cf_model

# TODO: - user log in or sign in?
# - ask new user for genre (3)
# - show random songs with max matching genre (later on, can rec from top rated matches)
# - ask for rating (not optional for new user)
# - update user emotion
# - ask new user for fav songs(3) (optional)
# - rec by clustering the songs
# - ask for rating (not optional for new user)
# - update user emotion

# old user -> 2options
# 1- ask for recs according to a new song input (song_emotion)
# 2- rec based on old activity (user_emotion)
# TODO:  -testing

# taking user_id input from user

while True:
    userId = input("Enter your user Id: ")
    x = re.search("\W", userId)
    if x is not None:
        print("invalid username")
    else:
        break

new_user_flag = True
try:
    sql.insert_user_emotion(userId)
except sqlite3.IntegrityError:
    print("already exists")
    new_user_flag = False

# taking song_name and artist_name input from user and generate url if the song/artist exists
while True:
    songName = input("Your song name: ")
    artistName = input("Artist of the given song: ")
    url = input_model.request_artist_song_url(artistName, songName)
    songName = songName.title()
    artistName = artistName.title()
    if input_model.check_url_exist(url) == 1:
        try:
            sql.insert_song_table(songName, artistName)
        except sqlite3.IntegrityError:
            print("already played!")
        break

# asking the user to rate the input song
while True:
    rating = input("Enter rating 1-10: ")
    rating = int(rating)
    if 0 <= rating <= 10:
        try:
            sql.insert_song_user_rating(userId, songName, rating)
        except sqlite3.IntegrityError:
            sql.update_song_user_rating(userId, songName, rating)
        break

# scrape and clean lyrics
print(url)
# for i in range(1, 10):
while True:
    lyr = lyrics.scrape_song_lyrics(url)
    if lyr != '':
        break

lyr_lis = lyrics.clean_song(lyr)

# calculate emotion score
em_lis = text_emotion(lyr_lis)
try:
    tags = genre.get_genre(songName, artistName)
    sql.insert_song_emotion(songName, artistName, em_lis, tags)
except sqlite3.IntegrityError:
    print("emotion score already exists! ")

# update user emotion
sql.update_user_emotion(userId, em_lis, rating)

# rec_lis = clustering.song_rec_clustering(userId, songName, em_lis)

cf_list = cf_model.collaborativeFiltering(userId, songName, artistName)

# for rec in rec_lis:
#     if rec not in cf_list:
#         cf_list.append(rec)


song_rec(userId, songName, cf_list)
