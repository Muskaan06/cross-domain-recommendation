import csv
import pandas as pd
import artist_emotion


df = pd.read_csv("music-artist-names.csv")
columns=['artist_id','Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']

def append_csv(fileName,lis):

    with open(fileName,"a") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=columns)
            writer.writerow({
                'artist_id':lis[0],
                'Positive':lis[1],
                'Negative':lis[2],
                'Anger':lis[3],
                'Anticipation':lis[4],
                'Disgust':lis[5],
                'Fear':lis[6],
                'Joy':lis[7],
                'Sadness':lis[8],
                'Surprise':lis[9],
                'Trust':lis[10]
            })

for row in df.iterrows():
    aId = row[1]['artist_id']
    if 10000100 < aId < 1000102:
        aName = row[1]['artist_name']
        lis = artist_emotion.get_artist_emotion(aName)
        lis.insert(0,aId)
        lis = tuple(lis)
        append_csv("artist_emotion.csv",lis)