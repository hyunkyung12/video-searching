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

def a_word(word,table):

    corpus = [[word for word in line.split()] for line in table["subtitle"]]

    index = np.zeros(0)

    for i in range(len(table)):
        tmp = corpus[i]
        check = sum(np.array(tmp) == word)
        if check > 0:
            index = np.append(index,1)
        else:
            index =  np.append(index,0)

    result = table[index == 1][['url','start','end']]
    result = result.reset_index()[['url','start','end']]
    return result

def find(table, func,target_word):
    result = func(target_word,table)   
    result.to_csv(path + '/data/check_list.csv')
    return result

if __name__ == "__main__":

    if funct == 0:
        find(demo,a_word,input_w)


    
