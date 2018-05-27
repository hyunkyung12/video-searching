import pandas as pd
from selenium import webdriver

k=1 #몇번째로 이동할래

result = pd.read_csv("result.csv",engine='python')
result['start'] = [line.split(',')[0] for line in result.reset_index()['start'] ]

driver = webdriver.Chrome('/Users/hyunjinpark/documents/Tobigs/chromedriver')

seconds = []
for i in range(len(result)):
    timestr = result.reset_index()['start'][i].split(',')[0]
    ftr = [3600,60,1]
    second = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
    seconds.append(second)

goto = result.reset_index()['url'][k] + "&start=" + str(seconds[k])
driver.get(goto)