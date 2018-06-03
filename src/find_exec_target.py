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

def exec_find(word,table):
    result = table[['subtitle']].apply(lambda x: x.values[0].find(word),axis = 1 )
    result = table[['url','start','end']][result != -1]
    return result

def target_find(table, func,target):
    result = func(target,table)   
    result.to_csv(path + "/data/" +'check_list.csv')
    return result

if __name__ == "__main__":

    print("...strat")
    target_find(demo,exec_find,input_w)
    print("...end")


    
