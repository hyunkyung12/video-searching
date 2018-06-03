import pandas as pd
import numpy as np
import sys
import os

file_name = sys.argv[1]
funct = sys.argv[2]
input_w = sys.argv[3]

path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
demo = pd.read_csv( path + "/data/" + file_name +".csv" )
demo = demo.dropna()

#functions for find
def iter_in_s(s,words):
    for i in range(len(words)):
        if s.find(words[i]) == -1:
            return 0
    return 1

#options for find
def exec_word_find(word,table):
    result = table[['subtitle']].apply(lambda x: x.values[0].find(word),axis = 1 )
    result = table[['url','start','end']][result != -1]
    return result

def exec_words_find(words,table):
    words = words.split()
    result = table[['subtitle']].apply(lambda x: iter_in_s(x.values[0],words),axis = 1 )
    result = demo[['url','start','end','subtitle']][result == 1]
    return result

#find
def target_find(table, func,target):
    result = func(target,table)   
    result.to_csv(path + "/data" +'/check_list.csv')
    return result

if __name__ == "__main__":

    print("...strat")
    if funct == "0":
        print("finding_a_exec_word")
        target_find(demo,exec_word_find,input_w)
    elif funct == "1":
        print("finding_exec_words")
        target_find(demo,exec_words_find,input_w)
    print("...end")


    
