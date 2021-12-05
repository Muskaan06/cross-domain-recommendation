from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
df=pd.read_csv(r"C:\Users\sbgsa\OneDrive\Desktop\cross-domain-recommendation\output\emotion_score.csv")
data=df.iloc[:,5:]
labels=list(df['Song'])

kmeans = KMeans(n_clusters=3, random_state=0).fit(data)
n_clusters=3
pred_clusters= kmeans.labels_
cluster_labels=[[] for i in range(n_clusters)]
for i, j in enumerate(pred_clusters):
    cluster_labels[j].append(labels[i])
print(cluster_labels)
