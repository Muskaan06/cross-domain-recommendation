import math
import sys

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

# -- artist
# RandomForestRegressor(bootstrap=False, max_depth=90, max_features=10, n_estimators=200, verbose=10)
# mean squared error:  0.0698603619231155

# -- user
# RandomForestRegressor(bootstrap=False, max_depth=90, max_features=10,
#                       n_estimators=200, verbose=10)
# mean squared error:  0.3112389096960047

# -- total
# LogisticRegression(C=0.0018329807108324356, multi_class='ovr', penalty='l1',
#                    solver='liblinear', verbose=10)
# mean squared error:  10.180606528877728

y_artist = pd.read_csv('y_artist_temp.csv')
y_user = pd.read_csv('y_user_temp.csv')
df = pd.read_csv('compressed_merged_file.csv')
X_artist = pd.read_csv("x_artist1.csv")
X_user = pd.read_csv("x_user_temp1.csv")

e = sys.float_info.epsilon
df['rating'] = df['rating'].replace(255, 0)
df['rating'] = df['rating'] + e


def fix_rating(rate):
    return math.ceil(rate / 10)


X_artist = X_artist.sort_values(['user_id', 'artist_id'])
X_artist = X_artist.set_index(['user_id', 'artist_id'])
X_user = X_user.sort_values(['user_id', 'artist_id'])
X_user = X_user.set_index(['user_id', 'artist_id'])

y_artist = y_artist.sort_values(['user_id', 'artist_id'])
y_artist = y_artist.set_index(['user_id', 'artist_id'])
y_artist['rating'] = y_artist['rating'].apply(fix_rating)

y_user = y_user.sort_values(['user_id', 'artist_id'])
y_user = y_user.set_index(['user_id', 'artist_id'])
y_user['rating'] = y_user['rating'].apply(fix_rating)


def random_forest(X, y):
    y = y.values.ravel()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # print("-----train shape-----")
    # print(X_train.shape)
    # print(y_train.shape)
    # print("-----test shape-----")
    # print(X_test.shape)
    # print(y_test.shape)

    rf = RandomForestRegressor(bootstrap=False, max_depth=90, max_features=10, n_estimators=50, verbose=10)  # n_estimators=200
    rf.fit(X_train, y_train)
    print(rf.score(X_train, y_train))
    # y_pred = rf.predict(X_test)
    # print("mean squared error: ", mean_squared_error(y_test, y_pred))
    # return y_pred
    return rf


def logistic_reg(X, y):
    y = y.values.ravel()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # print("-----train shape-----")
    # print(X_train.shape)
    # print(y_train.shape)
    # print("-----test shape-----")
    # print(X_test.shape)
    # print(y_test.shape)

    lr = LogisticRegression(C=0.002, multi_class='ovr', penalty='l1', solver='liblinear')
    lr.fit(X_train, y_train)
    # y_pred = lr.predict(X_test)
    # print("mean squared error: ", mean_squared_error(y_test, y_pred))
    # return y_pred
    return lr


# TODO: use fresh X_user, X_artist, X, y to predict. (take the next few thousand users from the main dataset)
y_user_pred = random_forest(X_user, y_user).predict(X_user)
y_artist_pred = random_forest(X_artist, y_artist).predict(X_artist)
print(y_user_pred.shape)
print(y_artist_pred.shape)

y_user_pred = np.array(y_user_pred)
y_artist_pred = np.array(y_artist_pred)
X = np.vstack((y_user_pred, y_artist_pred)).T
print(X.shape)

y = df[['user_id', 'artist_id', 'rating']]
y = y.sort_values(['user_id', 'artist_id'])
y = y.set_index(['user_id', 'artist_id'])
y['rating'] = y['rating'].apply(fix_rating)

y_pred = logistic_reg(X, y).predict(X)
y = y.values.ravel()
print("accuracy: ", accuracy_score(y, y_pred))

# print(X_user.shape)
# print(X_artist.shape)
# print(y_user.shape)
# print(y_user.shape)
# print(y.shape)
