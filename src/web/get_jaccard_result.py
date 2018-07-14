import konlpy
from konlpy.tag import *
from konlpy.utils import pprint

import nltk

import io
import os
import pandas as pd
import numpy as np
import pickle
import json

from ast import literal_eval
from itertools import chain

from gensim.models import Word2Vec
from sklearn.metrics.pairwise import *

import sqlite3

# file_name = sys.argv[1]
# sentence = sys.argv[2]
# num = sys.argv[3]


# 2.
## 자카드 유사도
def jaccard(s1, s2):
    c = len(set(s1)&set(s2)) # s2 = set("Hello")이면 s2={'e', 'H', 'l', 'o'}
    return float(c) / (len(set(s1)|set(s2))) # float 소수점 포함

## subtitle 비교
def compare_subtitle_kkma(sentence, input_file, num): # 꼬꼬마로 index

    distance = []
    kkma = Kkma()
    print(len(input_file))
    for i in range(len(input_file)):
        distance.append(jaccard(kkma.morphs(sentence), input_file[i]))

    result = []
    for i in range(num):
        max_index = np.argmax(np.array(distance))
        if distance[max_index] == 0:
            return result
        distance[max_index] = -1
        result.append(max_index)
    return result

def write_csv():
    print(sentence)
    print(int(num))
    index = compare_subtitle_kkma(sentence, demo['morphs'], int(num))

    output = {}
    output['subtitle'] = demo['subtitle'][index]
    output['start'] = demo['start'][index]
    output['end'] = demo['end'][index]
    output['url'] = demo['url'][index]

    print(output['subtitle'])

    Output = pd.DataFrame(output).reset_index()
    Output.to_csv('data/jaccard_checklist.csv')


def write_json():
    csvfile = open('./data/jaccard_checklist.csv', 'r')

    jsonfile = open('file.json', 'w')

    fieldnames = ("num","url","start_time","end","subtitle")
    reader = csv.DictReader( csvfile, fieldnames)
    out = json.dumps( [ row for row in reader ] )
    jsonfile.write(out)

def read_json():

    write_json()
    with open('file.json', 'r') as f:
    #    txt = f.read()
        rtn = json.load(f)
    #rtn = json.load(txt)
    print("====================================")
    #print(rtn[1])
    print("====================================")

    #return json.dumps(rtn, ensure_ascii=False).encode('utf8')
    return rtn    

def make_new_json():
    
    check_list = read_json()

    print("====================================")
    #print(check_list)
    print("====================================")
   
    check_list = check_list[1:]
    url_list = [a['url'] for a in check_list]
    url_list = [c.replace('watch?v=','embed/') for c in url_list]
    url_list = [re.sub(r'&index?.*','',c) for c in url_list]
    url_list = [re.sub(r'&list?.*','',c) for c in url_list]

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
    while(i<len(check_list)):
        for c in count:
            sub_data = check_list[i:i+c]
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

    with open('new.json', 'r', encoding='utf-8') as f:
        rtn = json.load(f)
    print("====================================")
    #print(rtn['count'][0])
    print("====================================")

    return json.dumps(rtn, ensure_ascii=False).encode('utf8')


if __name__ == "__main__":
    con = sqlite3.connect()
    sql = "SELECT * FROM sentence_meta"
    demo = pd.read_sql(sql, con)

    demo['text_token'] = demo.apply(lambda row:literal_eval(row['text_token']), axis=1)
# 1. 파일 불러오기
    
