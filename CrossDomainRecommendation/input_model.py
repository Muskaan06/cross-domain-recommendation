# Make HTTP requests
import requests
# Scrape data from an HTML document
from bs4 import BeautifulSoup
# I/O
import os
# Search and manipulate strings
import re
import time
import json
import signal
from contextlib import contextmanager

# contains genius api token
with open('genius_api_token.txt') as f:
    GENIUS_API_TOKEN = f.read()
f.close()

print(GENIUS_API_TOKEN)

class TimeoutException(Exception): pass

# limit execution time of a fuction
@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

# for user input
def request_artist_song_url(artist_name, song_name):
    artist_name = artist_name.lower()
    song_name = song_name.lower()

    artist_name = re.sub(r'[^\w\s]', '', artist_name)
    song_name = re.sub(r'[^\w\s]', '', song_name)

    artist = artist_name.replace(' ', '-')
    artist = artist.capitalize()

    song = song_name.replace(' ', '-')
    base_url = 'https://genius.com'

    make_url = base_url + '/' + artist + '-' + song + '-' + 'lyrics'
    return make_url


# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    # print(GENIUS_API_TOKEN)
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


# Get Genius.com song url's from artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []

    while True:
        response = request_artist_info(artist_name, page)
        json_var = response.json()
        # Collect up to song_cap song objects from artist
        song_info = []
        song_title_tup = []
        for hit in json_var['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)

        # Collect song URL's from song objects
        for song in song_info:
            if len(songs) < song_cap:
                url = song['result']['url']
                songs.append(url)
                title = song['result']['title']
                song_title_tup.append((artist_name, url, title))
        if len(songs) == song_cap:
            break
        else:
            page += 1

    print('Found {} songs by {}'.format(len(songs), artist_name))
    return song_title_tup
