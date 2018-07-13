import pandas as pd
import numpy as np
import re
import os
import sqlite3

srt_dir = 'data/srt/'

con = sqlite3.connect('../../data/youtubing.db')
sql_read_subtitle_meta = "SELECT * FROM subtitle_meta"
srt_dataset = pd.read_sql(sql_read_subtitle_meta, con)

cur = con.cursor()
cur.execute("SELECT max(subtitle_token_id) FROM subtitle_token")
start_subtitle_token_id = cur.fetchall()
if start_subtitle_token_id[0][0] is None:
    start_subtitle_token_id = 0
else:
    start_subtitle_token_id = start_subtitle_token_id[0][0]

subtitle_token_id = start_subtitle_token_id

start = []
end = []
subtitle_token_id_list = []
subtitle_id_list = []
subtitle_string_processing = []

for j, row in srt_dataset.iterrows():
    if (j+1)%10 == 0:
        print('--- src/preprocessing/cleansing_subtitle.py cleansing_subtitle {}/{} ---'.format(j+1, len(srt_dataset)))
    if '.srt' not in row['filename']:
        continue

    try:
        with open(row['filename'], 'r', encoding='UTF8') as f: # srt_dir + 
            lines = f.read()
        
        for token in lines.split('\n\n'):
            if len(token.strip()) == 0:
                continue
            splited = token.split('\n')
            if(splited[0] == ''):                
                time = splited[2]
                s, _, e = time.split(' ')
                start.append(s)
                end.append(e)
                subtitle_string_processing.append(re.sub('<.*?>', "", ' '.join(splited[3:])))                
            elif(splited[0] != ''):
                time = splited[1]
                s, _, e = time.split(' ')
                start.append(s)
                end.append(e)
                if(len(splited) == 2):
                    subtitle_string_processing.append(re.sub('<.*?>', "", ''))
                else:
                    subtitle_string_processing.append(re.sub('<.*?>', "", ' '.join(splited[2:])))
            subtitle_id_list.append(row['subtitle_id'])
            subtitle_token_id += 1
            subtitle_token_id_list.append(subtitle_token_id)  
    except IOError:
        print("file io error")
        pass

data = pd.DataFrame({'subtitle_token_id' : subtitle_token_id_list, \
                           'start_time' : start, \
                           'end_time' : end, \
                           'subtitle_token' : subtitle_string_processing, \
                           'subtitle_id' : subtitle_id_list})

data = data.loc[data['subtitle_token'] != ' ',:]
data.to_sql('subtitle_token', con, if_exists='append', index=False)