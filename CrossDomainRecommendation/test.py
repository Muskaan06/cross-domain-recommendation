import pandas as pd
import numpy as np
from utils import database_update, database_update_user_input, read_file, convert_to_csv
from lyrics import scrape_song_lyrics, clean_song
from emotion_score import text_emotion


# df = pd.read_csv('/Users/muskaanmaurya/Documents/pycharm/pythonProject/dataset/data.csv')
# df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
# artist_name = df['artist'].unique()
# artist_name = artist_name.astype('str')
# artist_name = np.char.lower(artist_name)
#


file_name = "cross-domain-recommendation-master/cross-domain-recommendation-master/dataset/song_database.csv"

# test = database_update_user_input(artist_name, song_name, file_name)
lyric_list = list()
df = read_file(file_name)
# #
song_url = df['Lyrics_url'].tolist()
#
for url in song_url:
    print(url)
    lyric = scrape_song_lyrics(url)
    lyric = clean_song(lyric)
    lyric_list.append([lyric])

print(lyric_list)
df_lyric = pd.DataFrame(lyric_list,columns=['Cleaned_Lyrics'])
print(df_lyric)

result = pd.concat([df, df_lyric], axis=1).reindex(df.index)
convert_to_csv(result,"song_lyric_database.csv")

