# # import pandas as pd
# #
# # my_file = open(os.path.join(sys.path[0], '..', 'CrossDomainRecommendation', "genres.txt"), "r", encoding='iso-8859-1')
# #
# # str=""
# # for  in symps:
# #     str= str + "<option value=\"" + symp + "\">" + symp.title() + "</option>\n"
# #
# # print(str)
# import json
# flist = []
# val1 = ['hello', 'bye']
#     #doubleQString = "{0}".format(val)
#     #print(doubleQString)
# temp = json.dumps(val1)
#
#
# # for val in flist:
# #     print(eval(val))
# print(temp)

# import sql

# def genre_rec(genres):
#     song_genre, song_list = sql.fetch_song_genres()
#     idx_cnt_list = []
#     for i, gen_list in enumerate(song_genre):
#         count = 0
#         which = []
#         for j, gen in enumerate(genres):
#             if gen in gen_list:  # if the song has matching tags  TODO: check if word in string? like 'rock' in 'rock and roll'
#                 count += 1
#                 which.append(j)
#         if count != 0:
#             idx_cnt_list.append([song_list[i], count, which])
#             # idx_cnt_list.append([song_list[i], count])
#     idx_cnt_list = sorted(idx_cnt_list, key=lambda x: x[1], reverse=True)
#     rec_ids = [x[0] for x in idx_cnt_list]
#     print(idx_cnt_list)
#     return rec_ids[:10]


#print(genre.get_all_genres())

# print(genre_rec(['guitar', 'pop', 'rnb']))

import pandas as pd
import sys, math

df = pd.read_csv('merged_file.csv')
# print(df.head())
user_cnt = df['user_id'].value_counts()
user_cnt = user_cnt.sort_values(ascending=False)
user_cnt = user_cnt.iloc[:10000]
users = user_cnt.index.tolist()
# print(users)
# print(len(users))
new_df = df.loc[df['user_id'].isin(users)]

e = sys.float_info.epsilon
def fix_rating(rate):
    return int(math.ceil(rate / 10))

new_df['rating'] = new_df['rating'].replace(255, 0)

new_df['rating'] = new_df['rating'].apply(fix_rating)
new_df['rating'] = new_df['rating'] + e

df1 = new_df[['user_id', 'rating']].groupby('user_id').max('rating')
df1 = df1.sort_values('rating', ascending=False)
df1 = df1.loc[df1['rating']>8]
user_list = df1.index.tolist()
# print(user_list)
# print(len(set(new_df['user_id'])))
new_df = new_df.loc[new_df['user_id'].isin(user_list)]
# print(new_df)
# new_df.to_csv('comp_dataset.csv')

heard_artists = set(new_df['artist_id'])
artist_emotions = pd.read_csv('artist_emotion.csv')
# print(artist_emotions)
all_artists = set(artist_emotions['artist_id'])

unheard_artists = all_artists - heard_artists
print(unheard_artists)
# {1007809, 1003138, 1007142, 1000841, 1007593, 1005963, 1006285, 1004272, 1005297, 1000850, 1007568, 1003540, 1004153, 1006943}
# def get_artist_emotion(artist_id):
#     emo_list = list((artist_emotions.loc[artist_emotions['artist_id'] == artist_id]).iloc[0, 1:])
#     return emo_list
# print(get_artist_emotion(1009001))