from . import sql
from . import input_model
from . import lyrics
import psycopg2
from . import genre
from CrossDomainRecommendation.emotion_score import text_emotion
import re

def insert_new_song(userId, songName, artistName, rating):
# taking song_name and artist_name input from user and generate url if the song/artist exists
    while True:
        url = input_model.request_artist_song_url(artistName, songName)
        songName = songName.title()
        artistName = artistName.title()
        if input_model.check_url_exist(url) == 1:
            try:
                sql.insert_song_table(songName, artistName)
            except psycopg2.IntegrityError:
                print("already played!")
            break

    # asking the user to rate the input song
    try:
        sql.insert_song_user_rating(userId, songName, rating)
    except psycopg2.IntegrityError:
        sql.update_song_user_rating(userId, songName, rating)


    # scrape and clean lyrics
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
    except psycopg2.IntegrityError:
        print("emotion score already exists! ")