import psycopg2
import pandas as pd
import input_model
import sql
from CrossDomainRecommendation import lyrics, genre
from CrossDomainRecommendation.emotion_score import text_emotion

df = pd.read_csv(r"../dataset/songlist.csv", index_col=False, encoding='iso-8859-1')

print(df.head())

for row in df.iterrows():
    songName=row[1]['title']
    artistName=row[1]['artist']

    url = input_model.request_artist_song_url(artistName,songName)
    if input_model.check_url_exist(url)==1:
        # print(url)
        try:
            sql.insert_song_table(songName,artistName)
        except psycopg2.IntegrityError:
            print("already played!")
        #scrape and clean lyrics
        print(url)
        for i in range(1,10):
            lyr = lyrics.scrape_song_lyrics(url)
            if lyr != '':
                break

        lyr_lis = lyrics.clean_song(lyr)


        #calculate emotion score
        em_lis = text_emotion(lyr_lis)
        print(em_lis)
        try:
            tags = genre.get_genre(songName, artistName)
            sql.insert_song_emotion(songName, artistName, em_lis, tags)
        except psycopg2.IntegrityError:
            print("emotion score already exists! ")
