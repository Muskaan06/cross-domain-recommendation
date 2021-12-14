import re
import requests
from bs4 import BeautifulSoup
import emotion_score
import genre
import lyrics


# Get artist object from Genius API
def request_artist_info(artist_name):
    song_lis = list()
    base_url = 'https://genius.com/artists/'
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
    return song_lis, url_lis


# make a list of possible languages
COLUMN_STR = 'English (en)	Afrikaans (af)	Albanian (sq)	Amharic (am)	Arabic (ar)	Armenian (hy)	Azeerbaijani (' \
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
columns = COLUMN_STR.split("\t")
columns = [a.split(" ")[0] for a in columns]
columns = [word.lower() for word in columns]


def get_artist_emotion(artistName):
    artist_emotion = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    song_count = 0
    song_list, url_list = request_artist_info(artistName)
    for i in range(len(song_list)):
        english_flag = True
        song_name_str = song_list[i]
        song_url = url_list[i]
        print(song_url)
        tag_list = genre.get_genre(song_name_str, artistName)
        print("tag list: ", tag_list)
        for tag in tag_list:
            words = tag.split(" ")
            for wd in words:
                if wd in columns:
                    english_flag = False
                    break
        # add to emotion only if song is in english and tags are non empty
        if english_flag and len(tag_list) > 0:
            song_count += 1
            while True:
                lyr = lyrics.scrape_song_lyrics(song_url)
                if lyr != '':
                    break

            lyr_lis = lyrics.clean_song(lyr)
            song_emotion = emotion_score.text_emotion(lyr_lis)
            for j in range(10):
                artist_emotion[j] += song_emotion[j]
            print(song_emotion)

    # average artist emotion
    if song_count:
        artist_emotion = [a / song_count for a in artist_emotion]
    print('TOTAL ARTIST EMOTION', artist_emotion)
    return artist_emotion


artistName = input('enter favorite artist: ')
get_artist_emotion(artistName)
