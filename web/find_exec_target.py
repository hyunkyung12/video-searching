import pandas as pd
import numpy as np
import sys
import os
import csv
import json
#file_name = sys.argv[1]
#funct = sys.argv[2]
#input_w = sys.argv[3]

#path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#demo = pd.read_csv( path + "/data/" + file_name +".csv" )
#demo = demo.dropna()

# def upload_data():
# 	demo = pd.read_csv("./data/kor_sub.csv")

def exec_find(word,table):
    result = table[['subtitle']].apply(lambda x: x.values[0].find(word),axis = 1 )
    result = table[['url','start','end','subtitle']][result != -1]
    return result

def target_find(target):
#    result = func(target,table)
    demo = pd.read_csv("./data/kor_sub.csv")
    result = exec_find(target, demo)
    result.to_csv("./data/check_list.csv")
    return result
                            
def upload_check_list():
    # with open('./data/check_list.csv','r') as f:
    #     reader = csv.reader(f)
    #     global check
    #     check = list(reader)
    #     #check = np.array(fam)
    # return check
    csvfile = open('./data/check_list.csv', 'r')
    jsonfile = open('file.json', 'w')

    fieldnames = ("num","url","start_time","end","subtitle")
    reader = csv.DictReader( csvfile, fieldnames)
    out = json.dumps( [ row for row in reader ] )
    jsonfile.write(out)

    with open('file.json', 'r') as f:
    #    txt = f.read()
    	rtn = json.load(f)
    #rtn = json.load(txt)
    print("====================================")
    print(rtn[1])
    print("====================================")

    return json.dumps(rtn, ensure_ascii=False).encode('utf8')
    # return rtn
# if __name__ == "__main__":
#     target_find(demo, input_w)