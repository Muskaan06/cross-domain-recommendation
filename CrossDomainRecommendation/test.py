import sql
import input_model
import lyrics
import sqlite3
from emotion_score import text_emotion


while True:
    userId = input("Enter your user Id: ")
    if(userId != ''):
        break
try:
    sql.insert_user_emotion(userId)
except:
    print("already exists")


while True:
    songName = input("Your song name: ")
    artistName = input("Artist of the given song: ")
    url = input_model.request_artist_song_url(artistName,songName)
    if input_model.check_url_exist(url)==1:
        try:
            sql.insert_song_table(songName,artistName)
        except sqlite3.IntegrityError:
            print("already played!")
        break

rating = input("Enter rating 1-10: ")
try:
    sql.insert_song_user_rating(userId, songName, rating)
except sqlite3.IntegrityError:
    sql.update_song_user_rating(userId,songName,rating)

sql.display('user_emotion')
sql.display('song_table')
sql.display('song_user_rating')
sql.display('song_emotion')


print(url)
for i in range(1,10):
    lyr = lyrics.scrape_song_lyrics(url)
    if(lyr != ''):
        break;

lyr_lis = lyrics.clean_song(lyr)

print(lyr_lis)


text_emotion(lyr_lis)




