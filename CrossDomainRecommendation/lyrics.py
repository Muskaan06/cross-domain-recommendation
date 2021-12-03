import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import re
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize,sent_tokenize
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


#scraping the lyrics
def scrape_song_lyrics(url):
    lis=''
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
#     print(html)
    lyrics = html.find_all('div', class_='lyrics')
    for ly in lyrics:
        lis += ly.get_text(separator = " ").strip()
    #remove identifiers like chorus, verse, etc
    lis = re.sub(r'[\(\[].*?[\)\]]', '', lis)
    #remove empty lines
    lis = os.linesep.join([s for s in lis.splitlines() if s])
    return lis

# function will take in the lowercased text and then remove all the punctuation
def remove_punctuation(word):
    translator = str.maketrans('', '', string.punctuation)
    text_punct = word.translate(translator)
    return text_punct

# removing stopwords
def remove_stopwords(word):  # The function will   tokenize the result and then filter off  the stop_words
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(word)
    result = [word for word in word_tokens if word not in stop_words]
    return result

#to clean the song
def clean_song(song_lyric):
    song= song_lyric
    text=re.sub(r'\d+','',song)#removing numbers
    #lowercasing
    text_lower=text.lower()
    result=remove_punctuation(text_lower)
    lyrics=remove_stopwords(result)
    return lyrics

