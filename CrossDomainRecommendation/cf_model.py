import random

import numpy as np
import sql
import genre
from clustering import get_similar_users
from sklearn.cluster import KMeans
from k_means_constrained import KMeansConstrained
import math


def collaborativeFiltering(user_name, song_name, artist_name):
    song_id_input = sql.get_song_id_input(song_name, artist_name)
    print(song_id_input)
    # user_list_common = sql.get_user_list_common(song_id_input)
    user_list_common = get_similar_users(user_name)
    user_list_common.remove(user_name)
    print("common users: ", user_list_common)

    # song ids of all songs listened by similar users
    similar_user_songs = sql.get_user_song_matrix(user_list_common)
    similar_user_songs = list(set(similar_user_songs))

    song_emo = []
    for song_id in similar_user_songs:
        song_emo.append(sql.get_song_emotion(song_id))

    # cluster all songs listened by similar users
    data = song_emo
    labels = similar_user_songs
    data_len = len(data)
    size_min = 3
    size_max = 8
    max_cluster = math.floor(data_len / size_min)
    min_cluster = math.ceil(data_len / size_max)
    n_clusters = random.randint(min_cluster, max_cluster)
    # kmeans = KMeans(n_clusters, random_state=0).fit(data)
    kmeans = KMeansConstrained(n_clusters, size_min=size_min, size_max=size_max, random_state=0)
    data = np.array(data)
    kmeans.fit(data)
    emo_list = sql.get_song_emotion(song_id_input)
    print("song emo: ", emo_list)
    emo_array = np.array([emo_list])
    x = kmeans.predict(emo_array, size_min=None, size_max=None)

    pred_clusters = kmeans.labels_
    cluster_labels = [[] for i in range(n_clusters)]
    for i, j in enumerate(pred_clusters):
        cluster_labels[j].append(labels[i])

    trained_data = cluster_labels
    print(trained_data)
    rec_ids = trained_data[x[0]]
    print("recs--", rec_ids)
    return rec_ids

    # user_song_matrix[:] = (value for value in user_song_matrix if value != str(song_id_input))
    # user_song_matrix = np.array(user_song_matrix)
    #
    # (unique, counts) = np.unique(user_song_matrix, return_counts=True)
    # frequencies = np.asarray((unique, counts)).T
    #
    # sorted_frequency = frequencies[frequencies[:, 1].argsort()]
    # sorted_frequency = sorted_frequency[::-1]
    #
    # flag = 0
    # suggested_song_id = []
    # for sid in sorted_frequency:
    #     if flag >= 5:
    #         break
    #     suggested_song_id.append(int(sid[0]))
    #     flag = flag + 1
    #
    # int_lis = tuple(suggested_song_id)
    # int_list = str(int_lis)
    # sql.print_cf_output(int_list)
    # return suggested_song_id


# collaborativeFiltering('amisha', 'yellow', 'coldplay')

def genre_rec(genres):
    song_genre, song_list = sql.fetch_song_genres()
    idx_cnt_list = []
    for i, gen_list in enumerate(song_genre):
        count = 0
        for gen in genres:
            if gen in gen_list:  # if the song has matching tags  TODO: check if word in string? like 'rock' in 'rock and roll'
                count += 1
        if count != 0:
            idx_cnt_list.append([i, count])
    idx_cnt_list = sorted(idx_cnt_list, key=lambda x: x[1], reverse=True)
    rec_ids = [x[0] for x in idx_cnt_list]
    print(idx_cnt_list)
    return rec_ids


# print(genre.get_all_genres())

print(genre_rec(['guitar', 'pop', 'dance']))
