# Make HTTP requests
import requests
import re

# contains genius api token


# print(GENIUS_API_TOKEN)

# for user input
def check_url_exist(url):
    response = requests.get(url)
    if response.status_code == 200:
        print('Web site exists')
        return 1
    else:
        print('Web site does not exist')
        return 0

def request_artist_song_url(artist_name, song_name):
    artist_name = artist_name.lower()
    song_name = song_name.lower()

    artist_name = re.sub(r'[^\w\s]', '', artist_name)
    song_name = re.sub(r'[^\w\s]', '', song_name)

    artist = artist_name.replace(' ', '-')
    artist = artist.capitalize()

    song = song_name.replace(' ', '-')
    song = song.replace("'", "")
    song = song.replace("(", "")
    song = song.replace(")", "")
    base_url = 'https://genius.com'

    make_url = base_url + '/' + artist + '-' + song + '-' + 'lyrics'
    result_url = make_url
    return result_url

# print(request_artist_song_url('Enrique iglesias', "somebody's me"))
