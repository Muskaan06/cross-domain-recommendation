from sklearn.cluster import KMeans
import sql
from k_means_constrained import KMeansConstrained

user_emo, user_list = sql.fetch_user_emotion()

data = user_emo
labels = user_list
# user_id = 0

n_clusters = 3
kmeans = KMeansConstrained(n_clusters, size_min=2, size_max=None, random_state=0).fit(data)

pred_clusters = kmeans.labels_
cluster_labels = [[] for i in range(n_clusters)]
for i, j in enumerate(pred_clusters):
    cluster_labels[j].append(labels[i])

trained_data = cluster_labels

#
# def song_rec_clustering(userID, songN, emo_list):
#     # song_id = sql.get_song_id(songN)
#     user_emo = sql.get_user_emotion(userID)
#     y = kmeans.predict([user_emo])
#     x = kmeans.predict([emo_list])
#     rec_ids = trained_data[x[0]]
#     if y != x:
#         for val in trained_data[y[0]]:
#             rec_ids.append(val)
#     return rec_ids
#
#
def song_rec(userID,songN,rec_ids):
    user_ratings = sql.get_user_ratings(userID)
    song_id = sql.get_song_id(songN)
    for id in rec_ids:
        flag = 0
        if id == song_id: continue
        for rate in user_ratings:
            # if id != int(rate[0]): continue
            if int(id) == int(rate[0]):
                flag = 1  # found a match
                if rate[1] >= 5:  # old song -> update
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


print(trained_data)
for d in trained_data:
    print(len(d))


def get_similar_users(user_id, new_user=False):
    if new_user:
        emo_list = sql.get_user_emotion(user_id)
        x = kmeans.predict([emo_list])
        rec_ids = trained_data[x[0]]
    else:
        for cluster in trained_data:
            if user_id in cluster:
                rec_ids = cluster
    return rec_ids


# print(get_similar_users('muskaan06'))