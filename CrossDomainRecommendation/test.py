import sql
import input_model
import lyrics
import sqlite3
from emotion_score import text_emotion
import re
import clustering
import cf_model
import spotify_connect

#taking user_id input from user
while True:
    userId = input("Enter your user Id: ")
    x = re.search("\W", userId)
    if x != None:
        print("invalid username")
    else:
        break

try:
    sql.insert_user_emotion(userId)
except sqlite3.IntegrityError:
    print("already exists")

#taking song_name and artist_name input from user and generate url if the song/artist exists
while True:
    songName = input("Your song name: ")
    artistName = input("Artist of the given song: ")
    url = input_model.request_artist_song_url(artistName,songName)
    if input_model.check_url_exist(url)==1:
        try:
            sql.insert_song_table(songName.title(),artistName.title())
        except sqlite3.IntegrityError:
            print("already played!")
        break

#asking the user to rate the input song
while True:
    rating = input("Enter rating 1-10: ")
    rating = int(rating)
    if(rating>0 and rating<=10):
        try:
            sql.insert_song_user_rating(userId, songName, rating)
        except sqlite3.IntegrityError:
            sql.update_song_user_rating(userId,songName,rating)
        break;



#scrape and clean lyrics
print(url)
for i in range(1,10):
    lyr = lyrics.scrape_song_lyrics(url)
    if lyr != '':
        break

lyr_lis = lyrics.clean_song(lyr)


#calculate emotion score
em_lis = text_emotion(lyr_lis)
try:
    sql.insert_song_emotion(songName,em_lis)
except sqlite3.IntegrityError:
    print("emotion score already exists! ")


#update user emotion
# sql.update_user_emotion(userId, em_lis, rating)
#
# rec_lis = clustering.song_rec_clustering(userId, songName, em_lis)
#
# cf_list = cf_model.collaborativeFiltering(userId,songName.title(),artistName.title())
#
# for rec in rec_lis:
#     if rec not in cf_list:
#         cf_list.append(rec)
#
#
# clustering.song_rec(userId,songName,cf_list)
