# Music Recommendation
## Description

This is a model to recommend music based on the user's input song. We ask user for a song and it's artist's name. Then we do the sentiment analysis of the song's lyrics and finally cluster it in our database which recommends song to the user.

## Steps Involved

1. Generating url of the input song and checking it's validity.
2. Scraping the lyrics using [Genius API](https://genius.com/Ed-sheeran-shape-of-you-lyrics).
3. If the song is not present in out database, we add this song. Our database is dynamic which means that it will keep updating whenever it comes acorss a new song. **See song_database.csv in the output folder file**.
4. After scraping the lyrics, we do the sentiment analysis of the song by calculating emotion score using [NRC Emotion Lexicon](https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm) which contains the list of more than 14,000 words and their associations with eight basic emotions (anger, fear, anticipation, trust, surprise, sadness, joy, and disgust) and two sentiments (negative and positive). **See emotion_score.csv in the output folder file to get a clear idea**.
5. Next step involves making a cluster of each of these emotions and categorising the song into one of these such that the recommmended songs also belongs to the same cluster.
