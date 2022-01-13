import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD
# import seaborn as sns
import sys
import math

e = sys.float_info.epsilon

def fix_rating(rate):
    return int(math.ceil(rate / 10))


df = pd.read_csv('compressed_merged_file.csv')
df = df.drop('Unnamed: 0', axis=1)
df['rating'] = df['rating'].replace(255, 0)

df['rating'] = df['rating'].apply(fix_rating)
df['rating'] = df['rating'] + e
dataset = df.loc[df['user_id'].isin(list(range(1, 100)))]
# x = len(set(dataset['user_id']))
dataset = dataset[['user_id', 'artist_id', 'rating']]
# print(dataset.head)

# n_users = dataset.user_id.unique().shape[0]
# n_items = dataset.artist_id.unique().shape[0]
# n_items = dataset['artist_id'].max()
# A = np.zeros((n_users,n_items))
# for line in dataset.itertuples():
#     A[line[1]-1, line[2]-1] = line[3]
# print("Original rating matrix : ", A)

rating_crosstab = dataset.pivot_table(values='rating', index='user_id', columns='artist_id', fill_value=0)
print(rating_crosstab.head())
X = rating_crosstab.T

SVD = TruncatedSVD(n_components=12, random_state=5)
resultant_matrix = SVD.fit_transform(X)
print(resultant_matrix.shape)

corr_mat = np.corrcoef(resultant_matrix)
print(corr_mat.shape)

col_idx = rating_crosstab.columns.get_loc(1008916)
corr_specific = corr_mat[col_idx]
print(pd.DataFrame({'corr_specific':corr_specific, 'artist_id': rating_crosstab.columns}).sort_values('corr_specific', ascending=False).head(10))
