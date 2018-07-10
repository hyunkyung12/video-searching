import pandas as pd
import numpy as np
import sys
import os
import csv
import json
from collections import Counter

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

    #return json.dumps(rtn, ensure_ascii=False).encode('utf8')
    return rtn
# if __name__ == "__main__":
#     target_find(demo, input_w)

def make_new_json():
    
    aa = upload_check_list()

    print("====================================")
    print(aa)
    print("====================================")
   
    aa = aa[1:]
    url_list = [a['url'] for a in aa]

    cnt = Counter()
    for word in url_list:
        cnt[word] += 1
    cnt = list(cnt.items())

    cleaned = []

    for i in range(0,len(url_list)):
        if(i == len(url_list)-1):
            cleaned.append(url_list[i])
        else:
            if url_list[i] != url_list[i+1]:
                cleaned.append(url_list[i])

    count = []

    for url in cleaned:
        for c in cnt:
            if(c[0] == url):
                    count.append(c[1])

    data = {}  
    data['num'] = []  
    data['url'] = []  
    data['start_time'] = []  
    data['end_time'] = []  
    data['subtitle'] = []  
    data['count'] = []  

    i = 0
    j = 0
    while(i<len(aa)):
        for c in count:
#             print('when count is '+str(c)+' '+str(i)+':'+str(i+c))
#             i = i+c
            sub_data = aa[i:i+c]
            sub_num = []; sub_start = []; sub_end = []; sub_sub = [];
            for sub in sub_data:
                sub_num.append(sub['num'])
                sub_start.append(sub['start_time'])   
                sub_end.append(sub['end'])   
                sub_sub.append(sub['subtitle'])   
            data['num'].append(sub_num); data['start_time'].append(sub_start); 
            data['end_time'].append(sub_end); data['subtitle'].append(sub_sub); 
            data['count'].append(c)
            data['url'].append(cleaned[j])
            i = i+c  
            j = j+1


    with open('new.json', 'w') as outfile:
        json.dump(data, outfile)      
    #jsonfile = open('new.json', 'w')
    #out = json.dumps(data)
    #jsonfile.write(out)

    # print("====================================")
    # print(out)
    # print("====================================")

    with open('new.json', 'r', encoding='utf-8') as f:
    #    txt = f.read()
        rtn = json.load(f)
    #rtn = json.load(txt)
    print("====================================")
    print(rtn['count'][0])
    print("====================================")

    return json.dumps(rtn, ensure_ascii=False).encode('utf8')
    #return rtn