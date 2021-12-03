import nltk
import pandas as pd

nltk.download('punkt')
nltk.download('wordnet')
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import sqlite3

connection = sqlite3.connect('lexicon.db')

crsr = connection.cursor()

sql_command = """SELECT "English (en)", Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust
                    FROM NCR_lexicon"""

column = crsr.execute(sql_command)

tup_list = list()
for row in column:
    tup_list.append(row)
emolex_df = pd.DataFrame(tup_list,columns=['Word', 'Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust'])

# print(emolex_df)

# emolex_df = emo_lex[
#     ['English (en)', 'Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise',
#      'Trust']]
emotions = emolex_df.columns.drop('Word')
# emolex_df.rename(columns={'English (en)': 'word'}, inplace=True)


# for i in range(16):
#     song=data.iloc[i,4]
#     lyrics=re.sub('['+string.punctuation+']','',song)# removing punctuations
#     data.iat[i,4]=lyrics


# the function passes the column(col) of the respective dataframe passed as arguements
def text_emotion(lyric_list):
    listToStr = ' '.join(map(str, lyric_list))
   
    emo_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lemmatizer = WordNetLemmatizer()

    song = word_tokenize(listToStr)  # the body of text for each individual song(row)

    for word in song:
        new = lemmatizer.lemmatize(word)  # lemmatizing the words
        emo_score = emolex_df[emolex_df.Word == new]

        if not emo_score.empty:
            # for emotion in list(emotions):
            for index, em in enumerate(emotions):
                val = int(emo_list[index]) + int(emo_score[em])
                emo_list[index] = val


    return list(emo_list)

