from selenium import webdriver
from bs4 import BeautifulSoup #html 소스를 해부하기 위한 뷰숲
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame as df # dataframe 생성을 위함
import pandas as pd
import chardet # pandas와 함께 
import lxml #xml 처리 모듈인 lxml
import requests #크롤링 하려는 url의 response를 가져오기 위한 requests
import time # time.sleep을 위함
import csv
import re # 정규표현식
from urllib.request import urlopen
import sys
import os
import datetime
import sqlite3

keyword = "TED"
driver_path = "tools/chromedriver"
srt_download_path = "/path/srt/"
num_pagedown = 0

con = sqlite3.connect('data/youtubing.db')
sys.path.append(os.path.dirname(os.path.abspath(driver_path)))

# 다운로드 경로 설정
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : os.getcwd()+srt_download_path}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chromeOptions)

# 유투브 페이지 들어가서 '자막' 필터 된 '세바시' 입력
driver.get("https://www.youtube.com/results?sp=EgQQASgBQgQIARIA&search_query=" + keyword ) # 필터: 동영상+자막

print("--- src/crawling/get_subtitle.py START chromedriver ---")

## Youtube_search 최종
elm = driver.find_element_by_tag_name('html')

for j in range(num_pagedown):
    elm.send_keys(Keys.END)
    time.sleep(3)

time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

ad = soup.select('div.ytd-promoted-video-renderer > h3') # 광고
notices = soup.select('div.ytd-video-renderer > h3 > a')
notices2 = soup.select('ytd-thumbnail-overlay-time-status-renderer')
notices3 = soup.select('yt-formatted-string.ytd-video-meta-block')

print("--- src/crawling/get_subtitle.py START get video meta ---")

title = []
link = []
play_time = []
channel = []
if ad == []:
    for i in range(len(notices)):
        try:
            title.append(notices[i].get('title'))
            y = 'https://www.youtube.com'
            link.append(y + notices[i].get('href'))
            play_time.append(notices2[i].find(text=True).replace("\n","").replace(" ",""))    
            channel.append(notices3[i].find(text=True))
        except:
            None
    dataset = df({'title': title, 'url': link, 'play_time': play_time, 'channel_name': channel })

else:
    title.append(' ')
    link.append(' ')
    for i in range(len(notices)):
        try:
            title.append(notices[i].get('title'))
            y = 'https://www.youtube.com'
            link.append(y + notices[i].get('href'))
            play_time.append(notices2[i].find(text=True).replace("\n","").replace(" ",""))    
            channel.append(notices3[i].find(text=True))
        except:
            None
    link.pop()
    title.pop()
    dataset = df({'title': title, 'url': link, 'start_time': play_time, 'channel': channel })
    dataset = dataset.loc[dataset['title'] != ' ',:]

print("--- src/crawling/get_subtitle.py START get subtitle meta ---")

# 영상 URL로 downsub 사이트 들어가서 입력
link2 = []
data = []

y = 'http://downsub.com'
for i in range(len(dataset['url'])):
    try:
        data = re.sub('https://www.youtube.com/watch\?v\=','', dataset['url'][i])
        link2.append(y +'/?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D'+ data)
    except:
        None

    
srt_down = []
for i in range(len(link2)):
    r = requests.get(link2[i])
    s = BeautifulSoup(r.content, 'html.parser')
    
    b_list = s.findAll('b')
    
    lang = []
    for k in range(len(b_list)):
        lang.append(b_list[k].next_sibling)
    del lang[lang.index(' to:'):len(lang)]
    
    link_kor = []
    link_eng = []
    link_kor_auto = []
    link_eng_auto = []
    
    if "\xa0\xa0Korean" in lang:
        down1 = b_list[lang.index("\xa0\xa0Korean")]
        y = 'https://downsub.com'

        a = down1.find_all("a")
        a = re.sub('\[<a href=\"\.','',str(a))
        a = re.sub('\"\>\&gt\;&gt\;Download\&lt\;\&lt\;</a>\]','',str(a))
        a = re.sub('amp;','',str(a))
        
        
        link_kor.append(y + a)
    else: pass
    
    if "\xa0\xa0English" in lang:
        down2 = b_list[lang.index("\xa0\xa0English")]
        y = 'https://downsub.com'

        a = down2.find_all("a")
        a = re.sub('\[<a href=\"\.','',str(a))
        a = re.sub('\"\>\&gt\;&gt\;Download\&lt\;\&lt\;</a>\]','',str(a))
        a = re.sub('amp;','',str(a))

        link_eng.append(y + a)
    else: pass
    
    if "\xa0\xa0Korean (auto-generated)" in lang:
        down3 = b_list[lang.index("\xa0\xa0Korean (auto-generated)")]
        y = 'https://downsub.com'

        a = down3.find_all("a")
        a = re.sub('\[<a href=\"\.','',str(a))
        a = re.sub('\"\>\&gt\;&gt\;Download\&lt\;\&lt\;</a>\]','',str(a))
        a = re.sub('amp;','',str(a))
        
        link_kor_auto.append(y + a)
    else: pass
    
    if "\xa0\xa0English (auto-generated)" in lang:
        down3 = b_list[lang.index("\xa0\xa0English (auto-generated)")]
        y = 'https://downsub.com'

        a = down3.find_all("a")
        a = re.sub('\[<a href=\"\.','',str(a))
        a = re.sub('\"\>\&gt\;&gt\;Download\&lt\;\&lt\;</a>\]','',str(a))
        a = re.sub('amp;','',str(a))
        
        link_eng_auto.append(y + a)
    else: pass
    
    srt_down += link_kor + link_eng + link_kor_auto + link_eng_auto

print("--- src/crawling/get_subtitle.py START get subtitle files ({}) ---".format(len(srt_down))

# 자막 다운받기
num_of_srt = len(srt_down)
for i, down in enumerate(srt_down):
    driver.get(down)
    if not (i+1)%10:
        print("--- src/crawling/get_subtitle.py     GET subtitle file {}/{} ---".format(i+1, num_of_srt))

print("--- src/crawling/get_subtitle.py START save meta data (video, subtitle) ---")

# srt_dataset
date = []
explain = []
link = []
like = []
unlike = []
subscribe = []
hit = []

def num_parser(s):
    num = int(re.sub('[^0-9]', '', s))
    if '천' in s:
        num *= 1000
    elif '만' in s:
        num *= 10000
    return num

for i, url in enumerate(dataset['url']):
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    date_soup = soup.select('span.date')
    explain_soup = soup.select('yt-formatted-string.content')
    like_soup = soup.select('a.ytd-toggle-button-renderer')
    unlike_soup = soup.select('a.ytd-toggle-button-renderer')
    subscribe_soup = soup.select('span.yt-formatted-string')
    hit_soup = soup.select('span.yt-view-count-renderer')
    
    date.append(date_soup[0].find(text=True).replace('게시일: ',''))
    explain.append(explain_soup[0].find(text=True).split('\n\n')[0])
    like.append(num_parser(str(like_soup[0].findAll(text=True)[-1])))
    unlike.append(num_parser(str(unlike_soup[1].findAll(text=True)[-1])))
    subscribe.append(num_parser(str(subscribe_soup[0].find(text=True))))
    hit.append(num_parser(str(hit_soup[0].find(text=True).replace('조회수 ','').replace('회','').replace(',',''))))

    link.append(url)
   
    if not (i+1)%10:
        print("--- src/crawling/get_subtitle.py     GET subtitle meta {}/{} ---".format(i+1, (num_pagedown+1)*20))

dataset2 = df({'url' : link, 'uploaded_date' : date, 'summary' : explain, 'like_count' : like, 'unlike_count' : unlike, 'subscribe_count' : subscribe, 'hit_count' : hit, 'keyword' : keyword, 'created_date' : datetime.datetime.now().isoformat()})

srt_dataset = pd.merge(dataset,dataset2)

srt_dataset.to_sql('video_meta', con, if_exists='append', index=False)

con.close()
