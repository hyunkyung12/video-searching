import pandas as pd
from selenium import webdriver
import sys
import os

path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

k=1 #몇번째로 이동할래

result = pd.read_csv(path + "/data/check_list.csv")
result['start'] = [line.split(',')[0] for line in result.reset_index()['start'] ]

driver = webdriver.Chrome(path + '/chromedriver')

seconds = []
for i in range(len(result)):
    timestr = result.reset_index()['start'][i].split(',')[0]
    ftr = [3600,60,1]
    second = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
    seconds.append(second)

goto = result.reset_index()['url'][k] + "&start=" + str(seconds[k])
driver.get(goto)
