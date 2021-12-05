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
print(cluster_labels)

plt.scatter(data, labels)