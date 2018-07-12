import sys
import os

import pandas as pd
import numpy as np

import nltk

import konlpy
from konlpy.tag import *
from konlpy.utils import pprint

file_name = sys.argv[1]

#파일 불러오기
path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
demo = pd.read_csv( path + "/data/" + file_name +".csv" )
demo = demo.dropna()

kor_demo = demo[:1612]
kor_demo = kor_demo.reset_index()

eng_demo = demo[1612:]
eng_demo = eng_demo.reset_index()

del eng_demo['index']
del eng_demo['Unnamed: 0']

del kor_demo['index']
del kor_demo['Unnamed: 0']

##1.korean
#korea 형태소 분석 (kkma)
print("kkma ...")
kkma = Kkma()
kk_tag = kor_demo.apply(lambda row:kkma.pos(row['subtitle']), axis=1)
kor_demo['morphs'] = kor_demo.apply(lambda row:kkma.morphs(row['subtitle']), axis=1)
print("complete.\n")
#korea 형태소 분석 (명사, 동사)
print("kkma refined ...")
result = []
lst = ["NNG","NNP","NNB","NNM","NR","NP","VV","VA","VXV","VXA","VCP","VCN"]

for j in range(len(kor_demo)):
    indice = np.array( [ 1 if v in lst else 0 for (k,v) in kk_tag[j]] )
    temp = list(np.array(kor_demo['morphs'][j])[np.array(indice,dtype = bool)])
    result.append(temp)
    
kor_demo['refined_morphs'] = result
print("complete.\n")
##2.English
#english 형태소 분석 nltk
print("nltk ...")
eng_demo['morphs'] = eng_demo.apply(lambda row: nltk.word_tokenize(row['subtitle']), axis=1)
nltk_tag = eng_demo.apply(lambda row:nltk.pos_tag(nltk.word_tokenize(row['subtitle'])), axis=1)

result = []
lst = ["NN","NNP","NNPS","NNS","PRP","PRP$","VB","VBD","VBG","VBN","VBP","VBZ"]
print("complete.\n")
#english 형태소 분석 (명사, 동사)
print("nltk refined ...")
result = []
lst = ["NN","NNP","NNPS","NNS","PRP","PRP$","VB","VBD","VBG","VBN","VBP","VBZ"]

for j in range(len(eng_demo)):
    nltk_indice = np.array( [ 1 if v in lst else 0 for (k,v) in nltk_tag[j]] )
    nltk_temp = list(np.array(eng_demo['morphs'][j])[np.array(nltk_indice,dtype = bool)])
    result.append(nltk_temp)
    
eng_demo['refined_morphs'] = result
print("complete.\n")
##3.merge
kor_demo['lan'] = list(np.zeros(len(kor_demo),dtype = int) + 1)
eng_demo['lan'] = list(np.zeros(len(eng_demo),dtype = int))

frames = [kor_demo,eng_demo]
result = pd.concat(frames)

result = result.reset_index()
#저장
result.to_csv(path +"/data/morphs.csv")
