
import numpy as np
import sql

def collaborativeFiltering(user_name, song_name, artist_name):
    song_id_input = sql.get_song_id_input(song_name,artist_name)
    print(song_id_input)
    user_list_common = sql.get_user_list_common(song_id_input)
    # print(user_list_common)


    user_song_matrix = sql.get_user_song_matrix(user_list_common)

    user_song_matrix[:] = (value for value in user_song_matrix if value != str(song_id_input))
    user_song_matrix = np.array(user_song_matrix)

    (unique, counts) = np.unique(user_song_matrix, return_counts=True)
    frequencies = np.asarray((unique, counts)).T

    sorted_frequency = frequencies[frequencies[:, 1].argsort()]
    sorted_frequency = sorted_frequency[::-1]

    flag = 0
    suggested_song_id = []
    for sid in sorted_frequency:
        if (flag >= 5):
            break
        suggested_song_id.append(int(sid[0]))
        flag = flag + 1

    int_lis = tuple(suggested_song_id)
    int_list = str(int_lis)
    sql.print_cf_output(int_list)
    return suggested_song_id

# collaborativeFiltering('gaurav','Your Love Is My Drug','Kesha')