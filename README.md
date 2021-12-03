# Music Recommendation
## Description

This is a model to recommend music based on the user's input song. We ask user for a song and it's artist's name. Then we do the sentiment analysis of the song's lyrics and finally cluster it in our database which recommends song to the user.

## Steps Involved

1. Generating url of the input song and checking it's validity.
2. Scraping the lyrics using [Genius API](https://genius.com/Ed-sheeran-shape-of-you-lyrics).
3. If the song is not present in out database, we add this song. Our database is dynamic which means that it will keep updating whenever it comes acorss a new song.
4. After scraping the lyrics, we do the sentiment analysis of the song by calculating emotion score using [NRC Emotion Lexicon](https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm) which contains the list of more than 14,000 words and their associations with eight basic emotions (anger, fear, anticipation, trust, surprise, sadness, joy, and disgust) and two sentiments (negative and positive). 
5. Next step involves making a cluster of each of these emotions and categorising the song into one of these such that the recommmended songs also belongs to the same cluster.


##Updated:

###created 4 database tables:

1. **user_emotion**: keep track of each user and their emotion score after listening to each song. This is the main table for users.
2. **song_table**: keep track of all the songs being listened by the user. This is the main table for songs only.
3. **song_emotion**: keep track of emotion scores of each song.
4. **song_user_rating**: this is the bridge table which links users and songs. This table will store the songId each time any user listens to a new song. The user rates the song everytime they are listening and we take the average rating of the user along with the number of times that song had been played by that particular user.

These databases where created using **sqlite3.**

###added new files:

We have inserted 3 new files in this update: sql.py, creation_sql.py and lexicon_db.py

**sql.py**: contains unique methods for inserting elements in each of the database tables.
**creation_py**: contains sql queries for creation of each of the above tables.
**lexicon_db.py**: contains code for the connection of the NCR_lexicon database which was convert from .xlx.

After shifting to SQL, changes where made to test.py and emotion_score.py files accordingly.


