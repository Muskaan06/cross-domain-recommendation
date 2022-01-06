# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
#
# client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# sp1 = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read",client_id=cid,client_secret=secret,redirect_uri='https://edujtm.github.io/diversify/redirect'))
#
# # songName = input("Your song name: ")
# # artistName = input("Artist of the given song: ")
#
# def get_track_id():
#         # track_results = sp1.search(q='track:'+songName +' + '+ 'artist:'+artistName, type='track', limit=1)
#         # print(track_results)
#         track_results = sp1.search(q='track:Sugar + artist:Maroon 5', type='track', limit=1)
#         for i, t in enumerate(track_results['tracks']['items']):
#                 # if(t['name']==songName):
#                         return t['id']
#
# a = get_track_id()
# print(a)