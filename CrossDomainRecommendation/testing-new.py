import pandas as pd
import numpy as np
import math
import sys
from sklearn.cluster import KMeans
from k_means_constrained import KMeansConstrained
import random

e = sys.float_info.epsilon
def fix_rating(rate):
    return int(math.ceil(rate / 10))

df = pd.read_csv('compressed_merged_file.csv')
df = df.drop('Unnamed: 0', axis=1)
df['rating'] = df['rating'].replace(255, 0)

df['rating'] = df['rating'].apply(fix_rating)
df['rating'] = df['rating'] + e
dataset = df.loc[df['user_id'].isin(list(range(177, 10000)))]
x = len(set(dataset['user_id']))


# print(x)
# print(df.head)




#   1. Make test user, take out some highest rated songs to be separated, use other songs to build emotion of that user
#   2. Given that test user inputs a song, we recommend some of his highest rated songs or not - TESTING.

test_user = df.loc[df['user_id'] == 176]
test_user = test_user.sort_values('rating')
test_user = test_user.reset_index()
test_user = test_user.drop('index', axis=1)

test_user['rating'] = test_user['rating'].apply(fix_rating)
# print(len(test_user))
# pd.set_option('display.max_rows', test_user.shape[0]+1)
top_rated = test_user.tail(15)
test_user = test_user[:-15]

# print(test_user)
# print(top_rated)

x_user = test_user.drop('artist_id', axis=1)

x_user.loc[:, ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise',
               'Trust']] = x_user.loc[:,
                           ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness',
                            'Surprise', 'Trust']].multiply(x_user.loc[:, 'rating'], axis="index")

x_user = (x_user.groupby("user_id")).sum()

x_user.loc[:, ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise',
               'Trust']] = x_user.loc[:,
                           ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness',
                            'Surprise', 'Trust']].divide(x_user.loc[:, 'rating'], axis="index")
# print(x_user)

x_user = x_user.drop('rating', axis=1)
x_user = x_user.reset_index()

# print(x_user)
test_emo = list(x_user.iloc[0, 1:])
# print(test_emo)


def collaborativeFiltering(user_emo, artist_id):
    # song_name = song_name.title()
    # artist_name = artist_name.title()
    # song_id_input = sql.get_song_id_input(song_name, artist_name)
    # print(song_id_input)
    # if song_id_input == 0:
    #     insert_new_song(user_name, song_name, artist_name, rating)
    #     song_id_input = sql.get_song_id_input(song_name, artist_name)
    # # user_list_common = sql.get_user_list_common(song_id_input)

    user_list_common = get_similar_users(user_emo)
    # user_list_common.remove(user)
    print("common users: ", user_list_common)

    # song ids of all songs listened by similar users
    similar_user_artist, similar_user_artist_emotion = fetch_artist_id(user_list_common)
    # similar_user_artist = list(set(similar_user_artist))
    # print(similar_user_artist)

    # song_emo = []
    # for song_id in similar_user_songs:
    #     emo = sql.get_song_emotion(song_id)
    #     print(emo)
    #     song_emo.append(emo)

    # cluster all songs listened by similar users
    data = similar_user_artist_emotion
    labels = list(similar_user_artist)
    data_len = len(data)
    print(data_len)
    print(len(labels))
    size_min = 50
    size_max = 120
    max_cluster = math.floor(data_len / size_min)
    min_cluster = math.ceil(data_len / size_max)
    n_clusters = random.randint(min_cluster, max_cluster)
    # kmeans = KMeans(n_clusters, random_state=0).fit(data)
    kmeans = KMeansConstrained(n_clusters, size_min=size_min, size_max=size_max, random_state=0)
    data = np.array(data)
    # print(data)
    kmeans.fit(data)
    # print("Enter artist id:")

    # emo_list = sql.get_song_emotion(song_id_input)
    # print("song emo: ", emo_list)
    emo_list = list((df.loc[df['artist_id'] == artist_id]).iloc[0, 3:])
    emo_array = np.array([emo_list])
    # print(emo_array)
    x = kmeans.predict(emo_array, size_min=None, size_max=None)

    pred_clusters = kmeans.labels_
    print(pred_clusters)
    cluster_labels = [[] for i in range(n_clusters)]
    print('cluster labels--------',cluster_labels)
    print('labels ----',labels)
    for i, j in enumerate(pred_clusters):
        cluster_labels[j].append(labels[i])

    trained_data = cluster_labels
    # print(trained_data)
    rec_ids = trained_data[x[0]]
    print("recs---------------------------------------------------------------------------------------------------")
    print(set(rec_ids))
    list1=list(set(rec_ids))
    print("top rated ------------------")
    print(top_rated['artist_id'])
    list2 = list(top_rated['artist_id'])
    listf = set(list1) & set(list2)
    print("Common----",listf)
    return rec_ids


def fetch_artist_id(user_list):
    similar_user = dataset.loc[df['user_id'].isin(user_list)]
    artist_common = similar_user.drop(['user_id','rating'], axis=1)
    artist_common = artist_common.drop_duplicates()
    print("arieokjo0900000000000000000000000000000000000------------")
    print(artist_common)
    similar_artist_id = artist_common['artist_id']

    similar_artist_emotion = artist_common.iloc[:, 1:]
    similar_artist_emotion = similar_artist_emotion.values.tolist()
    # print("Fetching artist ids for similar users ---")
    print("len----",len(similar_artist_id))
    print(len(similar_artist_emotion))

    return similar_artist_id, similar_artist_emotion


def fetch_user_emotion():
    print('fetch user emotion ---------')
    x_user = dataset.drop('artist_id', axis=1)

    x_user.loc[:, ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise',
                   'Trust']] = x_user.loc[:,
                               ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness',
                                'Surprise', 'Trust']].multiply(x_user.loc[:, 'rating'], axis="index")

    x_user = (x_user.groupby("user_id")).sum()

    x_user.loc[:, ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise',
                   'Trust']] = x_user.loc[:,
                               ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness',
                                'Surprise', 'Trust']].divide(x_user.loc[:, 'rating'], axis="index")
    # print(x_user)

    x_user = x_user.drop('rating', axis=1)
    x_user = x_user.reset_index()
    # print(x_user)
    x_user_emo = x_user.iloc[:, 1:]
    x_user_emo = x_user_emo.values.tolist()
    x_user_id = list(x_user.iloc[:, 0])
    # print(x_user_emo)
    # print(x_user_id)
    return x_user_emo, x_user_id


# fetch_user_emotion()

def cluster_user():
    user_emo, user_list = fetch_user_emotion()

    data = user_emo
    labels = user_list
    user_id = 0

    n_clusters = 3
    kmeans = KMeansConstrained(n_clusters, size_min=2, size_max=None, random_state=0).fit(data)

    pred_clusters = kmeans.labels_
    cluster_labels = [[] for i in range(n_clusters)]
    for i, j in enumerate(pred_clusters):
        cluster_labels[j].append(labels[i])

    trained_data = cluster_labels
    return kmeans, trained_data


def get_similar_users(user_emo):
    kmeans, trained_data = cluster_user()
    emo_list = np.array(user_emo)
    x = kmeans.predict(np.array([emo_list]),size_min=None, size_max=None)
    rec_ids = trained_data[x[0]]
    # print(x)
    return rec_ids


collaborativeFiltering(test_emo, 1002404)
# print(dataset.loc[dataset['user_id'] == 176])