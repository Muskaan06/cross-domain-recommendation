import pandas as pd
import numpy as np
from utils import database_update, database_update_user_input
from lyrics import scrape_song_lyrics, clean_song

df = pd.read_csv('/Users/muskaanmaurya/Documents/pycharm/pythonProject/dataset/data.csv')
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
# artist_name = df['artist'].unique()
# artist_name = artist_name.astype('str')
# artist_name = np.char.lower(artist_name)
#
file_name = 'song_database.csv'

# for artist in artist_name:
#     result = database_update(artist,file_name)
#
# print(result)

artist_name = 'maroon 5'
song_name = 'animals'

test = database_update_user_input(artist_name, song_name, file_name)

song_url = test['Lyrics_url'].tolist()

lyric = scrape_song_lyrics(song_url[1])

print(clean_song(lyric))