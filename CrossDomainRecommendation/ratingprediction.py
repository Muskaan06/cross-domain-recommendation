
import pandas as pd
import numpy as np
import sys

e = sys.float_info.epsilon

df = pd.read_csv('compressed_merged_file.csv')

#18235363
df['rating'] = df['rating'].replace(255,0)
df['rating'] = df['rating'] + e

# #artist output
# y_artist = df[['user_id','artist_id','rating']]
# y_artist = y_artist.sort_values(['user_id','artist_id'])
# # y_artist = y_artist.set_index('user_id')
#
# temp = df[['artist_id','rating']]
# temp = (temp.groupby("artist_id")).mean()
# temp = temp.reset_index()
#
# y_artist_temp = y_artist.merge(temp,on='artist_id')
# y_artist_temp = y_artist_temp.drop('rating_x',axis=1)
# y_artist_temp.rename(columns={'rating_y':'rating'},inplace=True)

#artist input
x_artist = df.drop(["rating"],axis=1)
# x_artist = x_artist.drop_duplicates(ignore_index=True)
x_artist = x_artist.sort_values('artist_id')

print(x_artist.shape)

# #user output
# temp_user = df[['user_id','rating']]
# temp_user = (temp_user.groupby("user_id")).mean()
# temp_user = temp_user.reset_index()
#
# y_user_temp = y_artist.merge(temp_user,on='user_id')
# y_user_temp = y_user_temp.drop('rating_x',axis=1)
# y_user_temp.rename(columns={'rating_y':'rating'},inplace=True)
# print("---y_user_temp--")
# print(y_user_temp.shape)
#user input
df2 = df.drop('rating',axis=1)

#user input
x_user = df.drop('artist_id',axis=1)

x_user = x_user.sort_values('user_id')

x_user.loc[:,['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']] = x_user.loc[:,['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']].multiply(x_user.loc[:, 'rating'], axis="index")


x_user = (x_user.groupby("user_id")).sum()

x_user.loc[:,['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']] = x_user.loc[:,['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']].divide(x_user.loc[:, 'rating'], axis="index")
# print(x_user)

x_user = x_user.drop('rating',axis=1)
x_user = x_user.reset_index()
x_user_temp = df2.merge(x_user,on='user_id')
x_user_temp = x_user_temp.drop(['Positive_x', 'Negative_x', 'Anger_x', 'Anticipation_x', 'Disgust_x', 'Fear_x', 'Joy_x', 'Sadness_x', 'Surprise_x', 'Trust_x'],axis=1)
x_user_temp.rename(columns={'Positive_y': 'Positive',
                            'Negative_y':'Negative',
                            'Anger_y':'Anger',
                            'Anticipation_y':'Anticipation',
                            'Disgust_y':'Disgust',
                            'Fear_y':'Fear',
                            'Joy_y':'Joy',
                            'Sadness_y':'Sadness',
                            'Surprise_y':'Surprise',
                            'Trust_y':'Trust'},inplace=True)
print("---x_user_temp----")
print(x_user_temp.shape)

x_artist = x_artist.drop('Unnamed: 0',axis=1)
x_user_temp = x_user_temp.drop(['Unnamed: 0_x','Unnamed: 0_y'],axis=1)

x_user_temp.to_csv("x_user_temp1.csv",index=False)
x_artist.to_csv("x_artist1.csv",index=False)


# y_user_temp.to_csv("y_user_temp.csv",index=False)

# y_artist_temp.to_csv("y_artist_temp.csv",index=False)


