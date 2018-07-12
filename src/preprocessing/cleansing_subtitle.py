import pandas as pd
import numpy as np
import re
import os
import sqlite3

srt_dir = 'data/srt/'

con = sqlite3.connect('data/youtubing.db')
sql_read_subtitle_meta = "SELECT * FROM subtitle_meta"
srt_dataset = pd.read_sql(sql_read_subtitle_meta, con)

file_list = os.listdir(srt_dir)

final_data = pd.DataFrame()

for i, row in srt_dataset.iterrows():
    if (i+1)%10 == 0:
        print('--- src/preprocessing/cleansing_subtitle.py {}/{} ---'.format(i+1, len(srt_dataset)))
    if '.srt' not in row['filename']:
        continue
    #down_title = re.sub('[^가-힣0-9a-zA-Z]', '', m)
    #down_title = re.sub('DownSubcom', '', down_title)
    #down_title = re.sub('srt', '', down_title)
    #down_title = re.sub('1', '', down_title)
    
    #if srt_title == down_title:
    #for k in range(len(srt_dataset)):
    with open(srt_dir + row['filename'], 'r', encoding='UTF8'):
        lines = f.readlines()
    
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
            time += [{'Time' : srt[i]}]
        elif sub_re.search(srt[i]) :
            if sub_re.search(srt[i-1]) :
                next
            elif sub_re.search(srt[i+1]) :
                subtitle += [{'subtitle_token' : srt[i] + ' ' + srt[i+1]}]
                next
            else :
                subtitle += [{'subtitle_token' : srt[i]}]
        elif space_re.match(srt[i]):
            subtitle += [{'subtitle_token' : srt[i]}]
            next

    subtitle_string_processing = []
    lang = []
    for string_processing in subtitle:
        subtitle_string_processing += [{'subtitle_token' : re.sub('<.*?>',"",string_processing['subtitle_token'])}]
        #if len(re.compile('[^ㄱ-ㅣ가-힣]+').sub('',string_processing['subtitle_token'])) > 0:
        #    lang +=[{'language' : int(1)}]
        #else:
        #    lang += [{'language' : int(0)}]
    
    start = []
    end = []
    for i in range(len(time)):
        a = list(time[i].values())[0]
        b = a.split(' ')
        start += [{'start_time' : b[0]}]
        end += [{'end_time' : b[2]}]
        
    url = []
    title = []
    #for i in range(len(subtitle)):
        # url += [{'url' : srt_dataset['url'][k]}]
        #title += [{'title' : srt_dataset['title'][k]}]
        
    #data = pd.concat([pd.DataFrame(title), pd.DataFrame(url), pd.DataFrame(start), pd.DataFrame(end), pd.DataFrame(subtitle_string_processing), pd.DataFrame(lang)], axis = 1).iloc[:-1,]
    data = DataFrame({'subtitle_token_id' : subtitle_token_id_list, \
                      'start_time' : start, \
                      'end_time' : end, \
                      'subtitle_token' : subtitle, \
                      'subtitle_id' : subtitle_id_list})
    final_data = pd.concat([final_data, data], axis = 0)

final_data = final_data.loc[final_data['subtitle_token'] != ' ',:]
final_data = final_data.drop_duplicates(['title', 'subtitle_token', 'start_time'])

final_data.to_sql('subtitle_token', con, if_exists='append', index=False)