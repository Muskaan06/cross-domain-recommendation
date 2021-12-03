import sqlite3
import pandas as pd

connection = sqlite3.connect('lexicon.db')

emo_lex= pd.read_excel('/Users/muskaanmaurya/Desktop/CDR for music/NRC-Suite-of-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-v0.92-In105Languages-Nov2017Translations.xlsx')

emo_lex.to_sql('NCR_lexicon',connection,index=False)

connection.commit()
connection.close()
