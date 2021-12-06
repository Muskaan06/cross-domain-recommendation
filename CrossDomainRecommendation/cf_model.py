import pandas as pd
import scipy as sp
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

connection = sqlite3.connect('SongUser.db')
crsr = connection.cursor()

def collaborativeFiltering (user_name,song_name,artist_name):
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


    print(user_list_common)
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
        suggested_song_id.append(int(sid[0]))
        flag = flag + 1

    int_lis = tuple(suggested_song_id)
    int_list = str(int_lis)


    sql_command4 = """SELECT song_name,artist_name FROM song_table WHERE id in """ + int_list + ';'
    sdf = crsr.execute(sql_command4)

    # for row in sdf:
    #     print(row[0]," by ",row[1])

    return suggested_song_id

connection.commit()


