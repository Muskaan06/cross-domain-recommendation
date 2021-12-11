import requests
from bs4 import BeautifulSoup

ll=[]
song = input("song name: ")
artist = input("artist: ")

def genre_url(songName,artistName):
    songName = (songName.title()).strip()
    artistName = (artistName.title()).strip()
    songName = songName.replace(' ','+')
    artistName = artistName.replace(' ','+')

    g_url = 'https://www.last.fm/music/' + artistName + '/_/' + songName
    print(g_url)
    return g_url


def get_genre(songName,artistName):
    g_url = genre_url(songName,artistName)
    result = requests.get(g_url)
    html1 = BeautifulSoup(result.text, 'html.parser')
    lyrics = html1.find_all('li', class_='tag')
    # print(html1)
    for ly in lyrics:
        ll.append(ly.get_text(separator = " ").strip())
    return ll

print(get_genre(song,artist))