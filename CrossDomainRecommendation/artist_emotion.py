import os
import re

import requests
from bs4 import BeautifulSoup
import input_model

import lyrics
import emotion_score
import genre

with open('genius_api_token.txt') as f:
    GENIUS_API_TOKEN = f.read()
f.close()


# Get artist object from Genius API
def request_artist_info(artist_name):
    song_lis = list()
    base_url = 'https://genius.com/artists/'
    # headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    # search_url = base_url + '/search?per_page=10&page=' + str(page)
    # data = {'q': artist_name}
    artist_name = artist_name.lower()

    artist_name = re.sub(r'[^\w\s]', '', artist_name)

    artist = artist_name.replace(' ', '-')
    artist = artist.capitalize()

    search_url = base_url + artist
    print(search_url)
    response = requests.get(search_url)
    html = BeautifulSoup(response.text, 'html.parser')
    song = html.find_all('div', class_='mini_card-title')
    url_lis = []
    for a in html.find_all('a', class_='mini_card', href=True):
        url_lis.append(a['href'])
    for ly in song:
        song_lis.append(ly.get_text(separator=" ").strip())
    # remove identifiers like chorus, verse, etc
    return song_lis, url_lis


artistName = input("enter artist: ")
song_list, url_list = request_artist_info(artistName)

column_str = 'English (en)	Afrikaans (af)	Albanian (sq)	Amharic (am)	Arabic (ar)	Armenian (hy)	Azeerbaijani (' \
             'az)	Basque (eu)	Belarusian (be)	Bengali (bn)	Bosnian (bs)	Bulgarian (bg)	Catalan (ca)	' \
             'Cebuano (ceb)	Chinese (Simplified) (zh-CN)	Chinese (Traditional) (zh-TW)	Corsican (co)	Croatian (' \
             'hr)	Czech (cs)	Danish (da)	Dutch (nl)	English (en)	Esperanto (eo)	Estonian (et)	Finnish (' \
             'fi)	French (fr)	Frisian (fy)	Galician (gl)	Georgian (ka)	German (de)	Greek (el)	Gujarati (' \
             'gu)	Haitian Creole (ht)	Hausa (ha)	Hawaiian (haw)	Hebrew (iw)	Hindi (hi)	Hmong (hmn)	Hungarian (' \
             'hu)	Icelandic (is)	Igbo (ig)	Indonesian (id)	Irish (ga)	Italian (it)	Japanese (ja)	Javanese (' \
             'jw)	Kannada (kn)	Kazakh (kk)	Khmer (km)	Korean (ko)	Kurdish (ku)	Kyrgyz (ky)	Lao (lo)	Latin ' \
             '(la)	Latvian (lv)	Lithuanian (lt)	Luxembourgish (lb)	Macedonian (mk)	Malagasy (mg)	Malay (ms)	' \
             'Malayalam (ml)	Maltese (mt)	Maori (mi)	Marathi (mr)	Mongolian (mn)	Myanmar (Burmese) (my)	' \
             'Nepali (ne)	Norwegian (no)	Nyanja (Chichewa) (ny)	Pashto (ps)	Persian (fa)	Polish (pl)	Portuguese ' \
             '(Portugal, Brazil) (pt)	Punjabi (pa)	Romanian (ro)	Russian (ru)	Samoan (sm)	Scots Gaelic (' \
             'gd)	Serbian (sr)	Sesotho (st)	Shona (sn)	Sindhi (sd)	Sinhala (Sinhalese) (si)	Slovak (sk)	' \
             'Slovenian (sl)	Somali (so)	Spanish (es)	Sundanese (su)	Swahili (sw)	Swedish (sv)	Tagalog (' \
             'Filipino) (tl)	Tajik (tg)	Tamil (ta)	Telugu (te)	Thai (th)	Turkish (tr)	Ukrainian (uk)	Urdu (' \
             'ur)	Uzbek (uz)	Vietnamese (vi)	Welsh (cy)	Xhosa (xh)	Yiddish (yi)	Yoruba (yo)	Zulu (zu) '
columns = column_str.split("\t")
columns = [a.split(" ")[0] for a in columns]
columns = [word.lower() for word in columns]

artist_emotion = [0,0,0,0,0,0,0,0,0,0]
for i in range(len(song_list)):
    song_name_str = song_list[i]
    song_url = url_list[i]
    print(song_url)
    tag_list = genre.get_genre(song_name_str, artistName)
    print("tag list: ", tag_list)
    for tag in tag_list:
        words = tag.split(" ")
        for wd in words:
            if wd in columns:
                print("exists!")
    while True:
        lyr = lyrics.scrape_song_lyrics(song_url)
        if lyr != '':
            break

    lyr_lis = lyrics.clean_song(lyr)
    song_emotion = emotion_score.text_emotion(lyr_lis)
    for i in range(10):
        artist_emotion[i] += song_emotion[i]
    print(song_emotion)
print('TOTAL ARTIST EMOTION', artist_emotion)
