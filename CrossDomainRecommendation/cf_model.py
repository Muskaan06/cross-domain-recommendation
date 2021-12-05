import pandas as pd
import scipy as sp
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

user_name = input("enter you id: ")
song_name = input("enter song name: ")
artist_name = input("enter artist name: ")

connection = sqlite3.connect('song_user2.db')
crsr = connection.cursor()

sql_command1 = """SELECT id FROM song_table WHERE song_name=? and artist_name=?;"""
qwe = crsr.execute(sql_command1, (song_name,artist_name,))
song_id_input = 0
for row in qwe:
    song_id_input = row[0]

sql_command2 = """SELECT user_id FROM song_user_rating WHERE song_id=?;"""
abc = crsr.execute(sql_command2,(song_id_input,))
user_list_common = []
for row in abc:
    user_list_common.append(row[0])


user_song_matrix = []
for users in user_list_common:

    sql_command3 = """SELECT song_id from song_user_rating where user_id=?;"""
    efg  = crsr.execute(sql_command3,(users,))

    for row in efg:
        user_song_matrix.append(row[0])


user_song_matrix[:] = (value for value in user_song_matrix if value != str(song_id_input))
user_song_matrix = np.array(user_song_matrix)

(unique, counts) = np.unique(user_song_matrix, return_counts=True)
frequencies = np.asarray((unique, counts)).T

sorted_frequency = frequencies[frequencies[:,1].argsort()]
sorted_frequency = sorted_frequency[::-1]

flag = 0
suggested_song_id = []
for sid in sorted_frequency:
    if (flag>=5):
        break
    suggested_song_id.append(sid[0])
    flag = flag + 1

integer_map = map(int, suggested_song_id)
int_lis = map(int, integer_map)
int_lis = tuple(int_lis)
int_lis = str(int_lis)


sql_command4 = """SELECT song_name,artist_name FROM song_table WHERE id in """ + int_lis + ';';
sdf = crsr.execute(sql_command4)

for row in sdf:
    print(row[0]," by ",row[1])

connection.commit()
connection.close()
