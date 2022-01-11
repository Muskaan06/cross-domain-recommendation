import sql
import genre

rows = sql.get_song_table()

song_list = []

for row in rows:
    song_name = row[1]
    artist_name = row[2]
    song_list.append((song_name, artist_name))

for song in song_list:
    song_name = song[0]
    artist_name = song[1]
    tags = genre.get_genre(song_name, artist_name)
    sql.update_song_genre(song_name, artist_name, tags)

