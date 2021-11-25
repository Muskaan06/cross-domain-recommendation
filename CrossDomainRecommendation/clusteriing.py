from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
df=pd.read_csv(r"C:\Users\gaura\PycharmProjects\cross-domain-recommendation\output\emotion_score.csv")
emo=df.iloc[:,5:]

# X = np.array([[1, 2], [1, 4], [1, 0],[10, 2], [10, 4], [10, 0]])
kmeans = KMeans(n_clusters=2, random_state=0).fit(emo)
print(kmeans.labels_)
#a=kmeans.predict([[0, 0], [12, 3]])
# print(kmeans.cluster_centers_)
# print(a)
