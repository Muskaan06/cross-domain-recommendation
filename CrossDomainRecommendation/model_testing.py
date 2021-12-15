import csv
import pandas as pd
import artist_emotion

df = pd.read_csv("music-artist-names.csv")
columns = ['artist_id', 'Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness',
           'Surprise', 'Trust']


def append_csv(fileName, lis):
    with open(fileName, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writerow({
            'artist_id': lis[0],
            'Positive': lis[1],
            'Negative': lis[2],
            'Anger': lis[3],
            'Anticipation': lis[4],
            'Disgust': lis[5],
            'Fear': lis[6],
            'Joy': lis[7],
            'Sadness': lis[8],
            'Surprise': lis[9],
            'Trust': lis[10]
        })


CHECK_EMPTY_LIST = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def insert_emotions(lower, upper, filename):
    for row in df.iterrows():
        aId = row[1]['artist_id']
        if 1000000 + lower < aId < 1000000 + upper:
            aName = row[1]['artist_name']
            lis = artist_emotion.get_artist_emotion(aName)
            if lis != CHECK_EMPTY_LIST:
                lis.insert(0, aId)
                lis = tuple(lis)
                append_csv(filename, lis)


insert_emotions(10750, 10753, "artist_emotion_1010001.csv")
