import sql
import input_model
import utils


# # df = pd.read_csv('/Users/muskaanmaurya/Documents/pycharm/pythonProject/dataset/data.csv')
# # df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
# # artist_name = df['artist'].unique()
# # artist_name = artist_name.astype('str')
# # artist_name = np.char.lower(artist_name)
# #
file_name = '..//dataset//song_database.csv'
# # test push
#
# # test = database_update_user_input(artist_name, song_name, file_name)
# # lyric_list = list()
# df = read_file(file_name)
# # #
# # song_url = df['Lyrics_url'].tolist()
# #
# # for url in song_url:
# #     print(url)
# #     lyric = scrape_song_lyrics(url)
# #     lyric = clean_song(lyric)
# #     lyric_list.append([lyric])
# #
# # print(lyric_list)
# # df_lyric = pd.DataFrame(lyric_list,columns=['Cleaned_Lyrics'])
# # print(df_lyric)
# #
# # result = pd.concat([df, df_lyric], axis=1).reindex(df.index)
# # convert_to_csv(result,"song_lyric_database.csv")


userId = input("Enter your user Id: ")
try:
    sql.insert_user_emotion(userId)
except:
    print("already exists")

songName = input("Your song name: ")
artistName = input("Artist of the given song: ")
sql.insert_song_table(songName,artistName)

rating = input("Enter rating 1-10: ")
sql.insert_song_user_rating(userId,songName,rating)

input_model.request_artist_song_url(artistName,songName)
utils.database_update_user_input(artistName,songName,file_name)

sql.display('user_emotion')
sql.display('song_table')
sql.display('song_user_rating')
sql.display('song_emotion')


