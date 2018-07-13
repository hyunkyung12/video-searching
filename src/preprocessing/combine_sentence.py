import pandas as pd
import sys
import os
import re
import sqlite3

stop_time = 30
stop_length = 400
stop_word = ['.', '!', '?']
re_stop_word = '['
while(stop_word):
    re_stop_word += stop_word[-1]
    stop_word.pop()
re_stop_word += ']'
min_length = 7

con = sqlite3.connect('data/youtubing.db')

did_sql = "SELECT max(subtitle_id) AS a FROM sentence_meta"
did = pd.read_sql(did_sql, con)
if did['a'][0] is None:
    did['a'][0] = 0

sql = "SELECT * FROM subtitle_token WHERE subtitle_id >" + str(did['a'][0])
demo = pd.read_sql(sql, con)

def remove_parenthesis(s):
    s = re.sub('\([ 가-힣a-z0-9\']*\)','',s)
    s = re.sub('\[[ 가-힣a-z0-9\']*\]','',s)
    return s

def convert_strtime_to_inttime(st):
    h, m, s_ms = st.split(':')
    s, ms = s_ms.split(',')
    hour = int(h)
    minute = int(m)
    second = int(s)
    milsec = int(ms)
    return hour * 3600000 + minute * 60000 + second * 1000 + milsec

def convert_inttime_to_strtime(time):
    milsec = int(time % 1000)
    time -= milsec
    time /= 1000
    second = int(time % 60)
    time -= second
    time /= 60
    minute = int(time % 60)
    time -= minute
    time /= 60
    hour = int(time)
    return str(hour) + ':' + str(minute) + ':' + str(second) + ',' + str(milsec)

def Mr_check(sentence):
    p = re.compile('[A-Z][a-z]{0,4}\\.')
    tmp = p.search(sentence)
    if tmp:
        return tmp
    p_num = re.compile('[0-9]*\\.[0-9]+')
    tmp = p_num.search(sentence)
    if tmp:
        return tmp

def is_pm_or_am(sentence):
    p = re.compile('[ap]\\.m\\.')
    tmp = p.search(sentence)
    if tmp:
        return tmp
    p = re.compile('\\.\\.\\.')
    tmp = p.search(sentence)
    if tmp:
        return tmp


def combine_sentence(df, stop_time, stop_length, min_length):
    url_list = list(set(df['subtitle_id']))
    print("--- src/preprocessing/combine_sentence.py START combine sentence {} ---".format(len(url_list)))
    new_df = pd.DataFrame(columns=['subtitle_id', 'start_time', 'end_time', 'subtitle_token'])

    for i, url in enumerate(url_list):
        if (i+1) % 10 == 0:
            print("--- src/preprocessing/combine_sentence.py {}/{} ---".format(i+1, len(url_list)))
        sub_df = df[df['subtitle_id'] == url]
        sub_df = sub_df.reset_index()
        l = sub_df.shape[0]
        time = -1
        sentence = ""
        for i in range(l):
            start_time = sub_df['start_time'][i]
            end_time = sub_df['end_time'][i]
            subtitle = sub_df['subtitle_token'][i]
            
            # 괄호 처리
            subtitle = remove_parenthesis(subtitle)

            if len(sentence + subtitle) < min_length:
                time = convert_strtime_to_inttime(start_time)
                sentence += subtitle
                continue

            p = re.search(re_stop_word, subtitle)
            while(p):
                mrc = Mr_check(subtitle)
                if mrc:
                    sentence += subtitle[:mrc.end()]
                    subtitle = subtitle[mrc.end():]
                else:
                    tmp = is_pm_or_am(subtitle)
                    sep_ind = tmp.end() if tmp else p.end()
                    sentence += subtitle[:sep_ind]
                    if time == -1:
                        s_time = start_time
                    else:
                        s_time = convert_inttime_to_strtime(time)
                    new_df = new_df.append({'subtitle_id' : url, 'start_time' : s_time, 'end_time': end_time, 'subtitle_token' : sentence}, ignore_index=True)
                    subtitle = subtitle[sep_ind:]
                    sentence = ""
                    time = convert_strtime_to_inttime(s_time)
                p = re.search(re_stop_word, subtitle)

            if (time == -1 and sentence == "") or (len(subtitle.strip()) == 0):
                time = convert_strtime_to_inttime(start_time)
                sentence += subtitle
                continue
            sentence += ' ' + subtitle
            if convert_strtime_to_inttime(end_time) - time > stop_time * 1000 or len(sentence) > stop_length:
                new_df = new_df.append({'subtitle_id' : url, 'start_time' : convert_inttime_to_strtime(time), 'end_time': end_time, 'sentence' : sentence}, ignore_index=True)
                time = -1
                sentence = ""
        if not (time == -1 and sentence == ""):
            new_df = new_df.append({'subtitle_id' : url, 'start_time' : convert_inttime_to_strtime(time), 'end_time': end_time, 'sentence' : sentence}, ignore_index=True)
    return new_df


demo = combine_sentence(demo, stop_time, stop_length, min_length)

demo.to_sql('sentence_meta', con, if_exists='append', index=False)
