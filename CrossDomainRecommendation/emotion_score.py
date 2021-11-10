import pandas as pd
from tqdm import tqdm_notebook as tqdm
from tqdm import trange
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string
from utils import convert_to_csv

data = pd.read_csv("song_lyric_database.csv")

emo_lex=pd.read_excel('/Users/muskaanmaurya/Desktop/CDR for music/NRC-Suite-of-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-v0.92-In105Languages-Nov2017Translations.xlsx')

emolex_df=emo_lex[['English (en)','Positive','Negative','Anger','Anticipation','Disgust','Fear','Joy','Sadness','Surprise','Trust']]
emotions=emolex_df.columns.drop('English (en)')
emolex_df.rename(columns={'English (en)':'word'},inplace=True)

for i in range(16):
    song=data.iloc[i,4]
    lyrics=re.sub('['+string.punctuation+']','',song)# removing punctuations
    data.iat[i,4]=lyrics


# the function passes the column(col) of the respective dataframe passed as arguements
def text_emotion(song_df, col):
    new_song_df = song_df.copy()
    # new  dataframe that will store the emotion scores
    emo_df = pd.DataFrame(0, index=new_song_df.index, columns=emotions)
    lemmatizer = WordNetLemmatizer()

    with tqdm(total=len(list(new_song_df.iterrows()))) as pbar:
        for i, row in new_song_df.iterrows():
            pbar.update(1)  # update the progress bar
            song = word_tokenize(new_song_df.loc[i][col])  # the body of text for each individual song(row)

            for word in song:
                new = lemmatizer.lemmatize(word)  # lemmatizing the words
                emo_score = emolex_df[emolex_df.word == new]
                if not emo_score.empty:
                    for emotion in list(emotions):
                        emo_df.at[i, emotion] += emo_score[emotion]

        new_song_df = pd.concat([new_song_df, emo_df], axis=1)
        return new_song_df

final_df=text_emotion(data,'Cleaned_Lyrics')
final_df = final_df.drop(columns=['Cleaned_Lyrics'],axis=1)
convert_to_csv(final_df,"emotion_score.csv")
