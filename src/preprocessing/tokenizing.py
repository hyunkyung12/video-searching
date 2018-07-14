import sys
import os

import pandas as pd
import numpy as np

import nltk

import konlpy
from konlpy.tag import *
from konlpy.utils import pprint

import sqlite3

con = sqlite3.connect('data/youtubing_dev.db')

#파일 불러오기
sql_stc = "SELECT \
                A.sentence_id as sentence_id, \
                A.start_time as start_time, \
                A.end_time as end_time, \
                A.sentence as sentence, \
                A.text_token as text_token, \
                A.embedding_vector as embedding_vector, \
                A.subtitle_id as subtitle_id, \
                B.filename as filename, \
                B.language as lan, \
                B.is_auto_generated as is_auto_generated, \
                B.video_id as video_id \
           FROM sentence_meta as A JOIN subtitle_meta as B ON A.subtitle_id = B.subtitle_id "
demo = pd.read_sql(sql_stc, con)

kor_demo = demo[demo['lan'] == "korean"]
eng_demo = demo[demo['lan'] == "english"]
eng_demo = eng_demo.reset_index()


##1.korean
#korea 형태소 분석 (kkma)
print("kkma...")
print(len(kor_demo))

if len(kor_demo) != 0:
    
    kkma = Kkma()
    kk_tag = kor_demo.apply(lambda row:kkma.pos(row['sentence']), axis=1)
    kor_demo['morphs'] = kor_demo.apply(lambda row:kkma.morphs(row['sentence']), axis=1)
    print("complete.\n")
#korea 형태소 분석 (명사, 동사)
    print("kkma refined ...")
    result = []
    lst = ["NNG","NNP","NNB","NNM","NR","NP","VV","VA","VXV","VXA","VCP","VCN"]

    for j in range(len(kor_demo)):
        indice = np.array( [ 1 if v in lst else 0 for (k,v) in kk_tag.values[j]] )
        temp = list(np.array(kor_demo['morphs'].values[j])[np.array(indice,dtype = bool)])
        result.append(str(temp))
        
    kor_demo['text_token'] = result
print("complete.")
print("\n")

##2.English
#english 형태소 분석 nltk
print("nltk ...")
print(len(eng_demo))
if len(eng_demo != 0):
    
    eng_demo['morphs'] = eng_demo.apply(lambda row: nltk.word_tokenize(row['sentence']), axis=1)
    nltk_tag = eng_demo.apply(lambda row:nltk.pos_tag(nltk.word_tokenize(row['sentence'])), axis=1)
    print("complete.\n")

#english 형태소 분석 (명사, 동사)
    print("nltk refined ...")
    result = []
    lst = ["NN","NNP","NNPS","NNS","PRP","PRP$","VB","VBD","VBG","VBN","VBP","VBZ"]

    for j in range(len(eng_demo)):
        nltk_indice = np.array( [ 1 if v in lst else 0 for (k,v) in nltk_tag.values[j]] )
        nltk_temp = list(np.array(eng_demo['morphs'].values[j])[np.array(nltk_indice,dtype = bool)])
        result.append(str(nltk_temp))
        
    eng_demo['text_token'] = result
print("complete.\n")

##3.merge
kor_demo['lan'] = list(np.zeros(len(kor_demo),dtype = int) + 1)
eng_demo['lan'] = list(np.zeros(len(eng_demo),dtype = int))

frames = [kor_demo,eng_demo]
result = pd.concat(frames)

result = result.reset_index()

#저장
#result.to_csv("morphs.csv")

result.drop(['morphs'], axis=1)

del_sql = "DELETE FROM sentence_meta WHERE text_token IS null"
cur = con.cursor()
cur.execute(del_sql)

save_result = result[['sentence_id', 'start_time', 'end_time', 'sentence', 'text_token', 'subtitle_id']]
save_result.to_sql('sentence_meta', con, if_exists='append', index=False)
