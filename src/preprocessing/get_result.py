import konlpy
from konlpy.tag import *
from konlpy.utils import pprint

import nltk

import pickle
import os
import re
import io
import pandas as pd
import numpy as np

from ast import literal_eval
from itertools import chain

from gensim.models import Word2Vec
from sklearn.metrics.pairwise import *

file_name = sys.argv[1]
sentence = sys.argv[2]
tokenizing = sys.argv[3]
metric = sys.argv[4]
num = sys.argv[5]
model = sys.argv[6]

num = int(num)

path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
demo = pd.read_csv( path + "/data/" + file_name  + ".csv" )
print(len(demo))

#load w2v model
if model == 'w2v':
    print("load w2v model..")
    kor_w2v_model = Word2Vec.load(path + "/data/kor_w2v_model.model")
    eng_w2v_model = Word2Vec.load(path + "/data/eng_w2v_model.model")
    print("complete.")
elif model =='ft':
    print("load fastText model")
    pkl_file = open(path+ '/data/ft_vec1.pkl', 'rb')
    mydict1 = pickle.load(pkl_file)
    pkl_file.close()

    pkl_file2 = open(path + '/data/ft_vec2.pkl', 'rb')
    mydict2 = pickle.load(pkl_file2)
    pkl_file2.close()

    d = {}
    for k,v in mydict1.items():
        d[k] = v
        
    for k,v in mydict2.items():
        d[k] = v
    
    eng_w2v_model = Word2Vec.load(path + "/data/eng_w2v_model.model")
    print("complete")
    
del demo['Unnamed: 0']
del demo['index']

#string -> list
demo['morphs'] = demo.apply(lambda row:literal_eval(row['morphs']), axis = 1)
demo['refined_morphs'] = demo.apply(lambda row:literal_eval(row['refined_morphs']), axis = 1)

demo['w2v_vec'] = demo.apply(lambda row:literal_eval(row['w2v_vec']), axis = 1)
demo['r_w2v_vec'] = demo.apply(lambda row:literal_eval(row['r_w2v_vec']), axis=1)

demo['ft_vec'] = demo.apply(lambda row:literal_eval(row['ft_vec']), axis = 1)
demo['r_ft_vec'] = demo.apply(lambda row:literal_eval(row['r_ft_vec']), axis=1)

#kor/eng
kor_demo = demo[demo['lan'] == 1]
eng_demo = demo[demo['lan'] == 0]
eng_demo = eng_demo.reset_index()

del eng_demo['index']
del kor_demo['level_0']
del eng_demo['level_0']

def isHangul(text):
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
    return hanCount > 0

def w2v_seq2vec(lst,model):
    size = len(lst)
    result = np.zeros(300,dtype = int)
    
    for i in range(size):
        try:
            dummy = model.wv[lst[i]]
            tmp = [ x + y for x,y in zip(result,dummy) ]
            result = tmp
        except:
            continue
            
    for i in range(300):
        try:
            result[i] = result[i]/size
        except:
            continue

    return list(result)

def ft_seq2vec(lst,model):
    size = len(lst)
    result = np.zeros(300,dtype = int)
    
    for i in range(size):
        try:
            dummy = model[lst[i]]
            tmp = [ x + y for x,y in zip(result,dummy) ]
            result = tmp
        except:
            continue
            
    for i in range(300):
        try:
            result[i] = result[i]/size
        except:
            continue

    return list(result)


def target_index(my_list, cmp_lists, metric, num): # metric: euclidean_distances, cosine_distances, manhattan_distances
    distance = []

    for i in range(len(cmp_lists)):
        distance.append(metric([my_list],[cmp_lists[i]]))

    b= list(chain(*distance))
    c =list(chain(*b))

    result = []
    for i in range(num):
        min_index = np.argmin(np.array(c))
        c[min_index] = 9999
        result.append(min_index)
    return result

#input 문장의 영어 or 한국어 // refined or full 에 따른 구분
h = isHangul(sentence)

if h&(tokenizing == "refined"):
    print("한국어/refined...")
    checklist = kor_demo
    kkma = Kkma()
    kk_pos = kkma.pos(sentence)
    kk_morph = kkma.morphs(sentence)

    lst = ["NNG","NNP","NNB","NNM","NR","NP","VV","VA","VXV","VXA","VCP","VCN"]

    indice = np.array( [ 1 if v in lst else 0 for (k,v) in kk_pos] )
    temp = list(np.array(kk_morph)[np.array(indice,dtype = bool)])
    print(temp)
    if model == 'w2v':
        print('w2v')
        test = w2v_seq2vec(temp,kor_w2v_model)
        cmp_lists = list(kor_demo['r_w2v_vec'])
    else:
        print('fastText')
        test = ft_seq2vec(temp,d)
        cmp_lists = list(kor_demo['r_ft_vec'])        

    print(test)
    
elif h&(tokenizing != "refined"):
    print("한국어/full...")
    checklist = kor_demo
    kkma = Kkma()
    kk_morph = kkma.morphs(sentence)
    print(kk_morph)
    
    if model == 'w2v':
        print('w2v')
        test = w2v_seq2vec(kk_morph,kor_w2v_model)
        cmp_lists = list(kor_demo['w2v_vec'])
    else:
        print('fastText')
        test = ft_seq2vec(temp,d)
        cmp_lists = list(kor_demo['ft_vec'])        

    print(test)
    
elif (h==False) &(tokenizing == "refined"):
    print("영어/refined...")
    checklist = eng_demo
    nltk_morph = nltk.word_tokenize(sentence)
    nltk_tag = nltk.pos_tag(nltk_morph)

    lst = ["NN","NNP","NNPS","NNS","PRP","PRP$","VB","VBD","VBG","VBN","VBP","VBZ"]

    nltk_indice = np.array( [ 1 if v in lst else 0 for (k,v) in nltk_tag] )
    nltk_temp = list(np.array(nltk_morph)[np.array(nltk_indice,dtype = bool)])
    print(nltk_temp)
    test = w2v_seq2vec(nltk_temp,eng_w2v_model)
    cmp_lists = list(eng_demo['r_w2v_vec'])
    print(test)
    
else:
    print("영어/full...")
    checklist = eng_demo
    nltk_morph = nltk.word_tokenize(sentence)
    print(nltk_morph)
    test = w2v_seq2vec(nltk_morph,eng_w2v_model)
    cmp_lists = list(eng_demo['w2v_vec'])
    print(test)

if metric == 'ucli':
    metric = euclidean_distances
elif metric == 'cosine':
    metric = cosine_distances
else:
    metric = manhattan_distances
    
index = target_index(test,cmp_lists,metric,num)

output = {}
output['subtitle'] = checklist['subtitle'][index]
output['start'] = checklist['start'][index]
output['end'] = checklist['end'][index]
output['url'] = checklist['url'][index]

Output = pd.DataFrame(output).reset_index()
print(Output['subtitle'])

Output.to_csv(path+'/data/w2c_checklist.csv')
