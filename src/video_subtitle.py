import pandas as pd
import numpy as np
import re

### 한국자막 df 만들기
url_kor = pd.read_csv("URL_KOREAN.csv").drop('ȸ', axis=1)
final_data = pd.DataFrame()

for k in range(100):
    f = open("C:/Users/kdg95/Desktop/lang/python/tobigs project/Korean_sub_srt/"+str(k)+"회.srt",'r',encoding='UTF8')
    lines = f.readlines()
    f.close()
    
    srt = []
    for i in range(len(lines)):
        srt += {lines[i].replace('\n','')}
    
    time = []
    subtitle = []
    time_re = re.compile('..:..:..')
    sub_re = re.compile('[가-힣a-zA-Z]')
    space_re = re.compile(' ')
    for i in range(len(srt)):
        if time_re.search(srt[i]) :
            time += [{'time' : srt[i]}]
        elif sub_re.search(srt[i]) :
            if sub_re.search(srt[i-1]) :
                next
            elif sub_re.search(srt[i+1]) :
                subtitle += [{'subtitle' : srt[i] + ' ' + srt[i+1]}]
                next
            else :
                subtitle += [{'subtitle' : srt[i]}]
        elif space_re.match(srt[i]):
            subtitle += [{'subtitle' : srt[i]}]
            next
                
    start = []
    end = []
    for i in range(len(time)):
        a = list(time[i].values())[0]
        b = a.split(' ')
        start += [{'start' : b[0]}]
        end += [{'end' : b[2]}]
        
    url = []
    for i in range(len(subtitle)):
        url += [{'url' : url_kor['URL'][k]}]
    
    data = pd.concat([pd.DataFrame(url), pd.DataFrame(start), pd.DataFrame(end), pd.DataFrame(subtitle)], axis = 1).iloc[:-1,]
    final_data = pd.concat([final_data, data], axis = 0)

final_data = final_data.loc[final_data['subtitle'] != ' ',:]
final_data.to_csv('kor_sub.csv',encoding='UTF8')

### 영어 자막 df 만들기
url_eng = pd.read_csv("data/english_sub.csv").drop('Unnamed: 0', axis=1)
final_data2 = pd.DataFrame()

for k in range(1,101):
    f = open("C:/Users/kdg95/Desktop/lang/python/tobigs project/english_sub/english_sub/"+str(k)+".srt",'r',encoding='UTF8')
    lines = f.readlines()
    f.close()
    
    srt = []
    for i in range(len(lines)):
        srt += {lines[i].replace('\n','')}
    
    time = []
    subtitle = []
    time_re = re.compile('..:..:..')
    sub_re = re.compile('[가-힣a-zA-Z]')
    space_re = re.compile(' ')
    for i in range(len(srt)):
        if time_re.search(srt[i]) :
            time += [{'time' : srt[i]}]
        elif sub_re.search(srt[i]) :
            if q.search(srt[i-1]) :
                next
            elif sub_re.search(srt[i+1]) :
                subtitle += [{'subtitle' : srt[i] + ' ' + srt[i+1]}]
                next
            else :
                subtitle += [{'subtitle' : srt[i]}]
        elif space_re.match(srt[i]):
            subtitle += [{'subtitle' : srt[i]}]
            next
                
    start = []
    end = []
    for i in range(len(time)):
        a = list(time[i].values())[0]
        b = a.split(' ')
        start += [{'start' : b[0]}]
        end += [{'end' : b[2]}]
        
    url = []
    for i in range(len(subtitle)):
        url += [{'url' : url_eng['url'][k-1]}]
    
    data = pd.concat([pd.DataFrame(url), pd.DataFrame(start), pd.DataFrame(end), pd.DataFrame(subtitle)], axis = 1).iloc[:-1,]
    final_data2 = pd.concat([final_data2, data], axis = 0)

final_data2 = final_data2.loc[final_data2['subtitle'] != ' ',:]
final_data2.to_csv('data/eng_sub.csv',encoding='UTF8')