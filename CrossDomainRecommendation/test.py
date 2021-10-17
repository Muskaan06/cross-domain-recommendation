import pandas as pd
import numpy as np
from utils import database_update

df = pd.read_csv('/Users/muskaanmaurya/Documents/pycharm/pythonProject/dataset/data.csv')

artist_name = df['artist'].unique()
artist_name = artist_name.astype('str')
artist_name = np.char.lower(artist_name)

file_name = 'song_database.csv'

for artist in artist_name:
    result = database_update(artist,file_name)

print(result)