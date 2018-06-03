import pandas as pd
import numpy as np
import re

srt_list = pd.read_csv("/data/srt_list.csv", encoding='CP949')

final_data = pd.DataFrame()
for k in range(len(srt_list)):
    f = open("/data/"+srt_list['Title'][k]+'.srt','r',encoding='UTF8')
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
    
    subtitle_string_processing = []
    for string_processing in subtitle:
        subtitle_string_processing += [{'subtitle' : re.sub('<.*?>',"",string_processing['subtitle'])}]
    
    start = []
    end = []
    for i in range(len(time)):
        a = list(time[i].values())[0]
        b = a.split(' ')
        start += [{'start' : b[0]}]
        end += [{'end' : b[2]}]
        
    url = []
    for i in range(len(subtitle)):
        url += [{'url' : srt_list['Link'][k]}]
    
    data = pd.concat([pd.DataFrame(url), pd.DataFrame(start), pd.DataFrame(end), pd.DataFrame(subtitle_string_processing)], axis = 1).iloc[:-1,]
    final_data = pd.concat([final_data, data], axis = 0)

final_data = final_data.loc[final_data['subtitle'] != ' ',:]
final_data.to_csv('/data/subtitle_file.csv',encoding='UTF8')
subtitle_file = pd.read_csv("/data/subtitle_file.csv")