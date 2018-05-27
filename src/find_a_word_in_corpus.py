import pandas as pd
import numpy as np
import sys
import os

word = sys.argv[1]

path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

demo = pd.read_csv( path + "/data/kor_sub.csv" )
demo = demo.dropna()
corpus = [[word for word in line.split()] for line in demo["subtitle"]]

index = np.zeros(0)

for i in range(len(demo)):
    tmp = corpus[i]
    check = sum(np.array(tmp) == word)
    if check > 0:
        index = np.append(index,1)
    else:
        index =  np.append(index,0)

result = demo[index == 1][['url','start','end']]
result = result.reset_index()[['url','start','end']]
result.to_csv(path + '/data/check_list.csv')
