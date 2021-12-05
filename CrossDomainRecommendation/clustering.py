from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sql

song_emo, song_list = sql.fetch_song_emotion()

data = song_emo
labels = song_list

n_clusters = 10
kmeans = KMeans(n_clusters, random_state=0).fit(data)

pred_clusters = kmeans.labels_
cluster_labels = [[] for i in range(n_clusters)]
for i, j in enumerate(pred_clusters):
    cluster_labels[j].append(labels[i])

trained_data = cluster_labels


def song_rec(userID, songN, emo_list):
    song_id = sql.get_song_id(songN)
    x = kmeans.predict([emo_list])
    rec_ids = trained_data[x[0]]
    user_ratings = sql.get_user_ratings(userID)

    for id in rec_ids:
        flag = 0
        if id == song_id: continue
        for rate in user_ratings:
            # if id != int(rate[0]): continue
            if id == int(rate[0]):
                flag = 1  # found a match
                if (rate[1] >= 5):  # old song -> update
                    songN = sql.display_song_rec(id)
                    print('Rate this recommendation 1-10 :')
                    rating = float(input())
                    sql.update_song_user_rating(userID, songN, rating)
                    song_emo = sql.get_song_emotion(id)
                    sql.update_user_emotion(userID, song_emo, rating)
                break
        if flag == 0:  # new song, insert
            songN = sql.display_song_rec(id)
            print('Rate this recommendation 1-10 :')
            rating = float(input())
            sql.insert_song_user_rating(userID, songN, rating)

            song_emo = sql.get_song_emotion(id)
            sql.update_user_emotion(userID, song_emo, rating)

    # trained_data[x[0]].append(song_id)

    # print(trained_data)
