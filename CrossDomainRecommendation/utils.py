import pandas as pd
from input_model import time_limit,request_song_url,TimeoutException
import csv
import os

song_df = pd.DataFrame(columns=["Artist", "Lyrics_url","Song"])
song_df.to_csv('song_database.csv',header=True)

def read_file(file_name):
    if(os.path.isfile(file_name)):
        data_read = pd.read_csv(file_name)
        data_read.drop(data_read.columns[data_read.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        return data_read
    else:
        print("database doesn't exist! ")
        return song_df


def convert_to_csv(dataframe, file_name):
    if(os.path.isfile(file_name)):
        os.remove(file_name)
        dataframe.to_csv(file_name,header=True)
    else:
        dataframe.to_csv(file_name,header=True)


def database_update(artist, file_name):
    song_df = read_file(file_name)

    try:
        with time_limit(7):
            new_tup = request_song_url(artist, 3)
            df = pd.DataFrame(new_tup, columns=["Artist", "Lyrics_url", "Song"])
            song_df = pd.concat([df, song_df])
    except TimeoutException as e:
        print("{} not found!".format(artist))
        dic = {"Artist": artist, "Lyrics_url": 'NaN', "Song": 'NaN'}
        song_df = song_df.append(dic, ignore_index=True)

    song_df.drop_duplicates(keep=False, inplace=True)
    convert_to_csv(song_df, file_name)
    return song_df

