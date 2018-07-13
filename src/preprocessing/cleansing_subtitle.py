import pandas as pd
import numpy as np
import re
import os
import sqlite3

srt_dir = 'data/srt/'

con = sqlite3.connect('data/youtubing.db')
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
    row['filename'] = row['filename'].replace('.crdownload', '')

    with open(srt_dir+row['filename'], 'r', encoding='UTF8') as f: 
        lines = f.read()
    
    for token in lines.split('\n\n'):
        token = token.strip()
        if len(token) == 0:
            continue
        if token[0] == '\n':
            token = token[1:]

        subtitle_token_id += 1
        subtitle_token_id_list.append(subtitle_token_id)
        _, time, *subtitle_token = token.split('\n')
        s, _, e = time.split(' ')
        start.append(s)
        end.append(e)
        subtitle_string_processing.append(re.sub('<.*?>', "", ' '.join(subtitle_token)))
        subtitle_id_list.append(row['subtitle_id'])

data = pd.DataFrame({'subtitle_token_id' : subtitle_token_id_list, \
                           'start_time' : start, \
                           'end_time' : end, \
                           'subtitle_token' : subtitle_string_processing, \
                           'subtitle_id' : subtitle_id_list})

data = data.loc[data['subtitle_token'] != ' ',:]
data.to_sql('subtitle_token', con, if_exists='append', index=False)
