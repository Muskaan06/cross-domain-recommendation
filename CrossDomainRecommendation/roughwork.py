# # import pandas as pd
# #
# # my_file = open(os.path.join(sys.path[0], '..', 'CrossDomainRecommendation', "genres.txt"), "r", encoding='iso-8859-1')
# #
# # str=""
# # for  in symps:
# #     str= str + "<option value=\"" + symp + "\">" + symp.title() + "</option>\n"
# #
# # print(str)
# import json
# flist = []
# val1 = ['hello', 'bye']
#     #doubleQString = "{0}".format(val)
#     #print(doubleQString)
# temp = json.dumps(val1)
#
#
# # for val in flist:
# #     print(eval(val))
# print(temp)

import sql

def genre_rec(genres):
    song_genre, song_list = sql.fetch_song_genres()
    idx_cnt_list = []
    for i, gen_list in enumerate(song_genre):
        count = 0
        which = []
        for j, gen in enumerate(genres):
            if gen in gen_list:  # if the song has matching tags  TODO: check if word in string? like 'rock' in 'rock and roll'
                count += 1
                which.append(j)
        if count != 0:
            idx_cnt_list.append([song_list[i], count, which])
            # idx_cnt_list.append([song_list[i], count])
    idx_cnt_list = sorted(idx_cnt_list, key=lambda x: x[1], reverse=True)
    rec_ids = [x[0] for x in idx_cnt_list]
    print(idx_cnt_list)
    return rec_ids[:10]


#print(genre.get_all_genres())

# print(genre_rec(['guitar', 'pop', 'rnb']))
