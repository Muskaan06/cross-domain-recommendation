# import pandas as pd
#
# my_file = open(os.path.join(sys.path[0], '..', 'CrossDomainRecommendation', "genres.txt"), "r", encoding='iso-8859-1')
#
# str=""
# for  in symps:
#     str= str + "<option value=\"" + symp + "\">" + symp.title() + "</option>\n"
#
# print(str)
import json
flist = []
val1 = ['hello', 'bye']
    #doubleQString = "{0}".format(val)
    #print(doubleQString)
temp = json.dumps(val1)


# for val in flist:
#     print(eval(val))
print(temp)