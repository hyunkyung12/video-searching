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

file_name = sys.argv[1]
sentence = sys.argv[2]
num = sys.argv[3]

# 1. 파일 불러오기
path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
demo = pd.read_csv( path + "/data/morphs.csv" )
demo = demo.dropna()

del demo['Unnamed: 0']
del demo['index']

demo['morphs'] = demo.apply(lambda row:literal_eval(row['morphs']), axis=1)
demo['refined_morphs'] = demo.apply(lambda row:literal_eval(row['refined_morphs']), axis=1)

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
Output.to_csv( path +'/data/jaccard_checklist.csv')
