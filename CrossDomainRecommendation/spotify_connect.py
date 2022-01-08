# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
#
# cid = '5f9054e7c5484b1996ab8f54b97e3156'
# secret = '81e74abdded4428da073591e14e57884'
#
# client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# # sp1 = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read",client_id=cid,client_secret=secret,redirect_uri='https://edujtm.github.io/diversify/redirect'))
#
#
# def get_track_id(songName, artistName):
#     # track_results = sp1.search(q='track:'+songName +' + '+ 'artist:'+artistName, type='track', limit=1)
#     # print(track_results)
#     # track_results = sp.search(q='track:Sugar + artist:Maroon 5', type='track', limit=1)
#     query = 'track:' + songName
#     track_results = sp.search(q=query, type='track')
#     print(track_results)
#     for i, item in enumerate(track_results['tracks']['items']):
#         for j, t in enumerate(item['artists']):
#             print(t['name'])
#             if t['name']==artistName:
#                 return t['id']
#
#
# # songName = input("Your song name: ")
# # artistName = input("Artist of the given song: ")
# a = get_track_id("I Got You", "Bebe Rexha")
# print(a)
# # https://open.spotify.com/track/4vVTI94F9uJ8lHNDWKv0i2?si=203bf4eeda0f4b30

import requests
import base64
import json
import urllib.parse
import os

# Step 1 - Authorization
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}


clientId = os.environ['CLIENTID']
clientSecret = os.environ['CLIENTSECRET']
# Encode as Base64
message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')


headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']
# Step 2 - Use Access Token to call search endpoint
def get_track_id(title,artist):
    title = title.replace("'", " ")
    artist = artist.replace("'", " ")
    title = urllib.parse.quote_plus(title)
    artist = urllib.parse.quote_plus(artist)
    query = 'track%3A'+title+'%20artist%3A%20'+artist+'&type=track&limit=1'
    searchUrl = f"https://api.spotify.com/v1/search?q={query}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)
    track_results = res.json()

    for i, item in enumerate(track_results['tracks']['items']):
        return item['id']


# print(get_track_id("I Got You", "Bebe Rexha"))
