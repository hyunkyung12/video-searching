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

keyword = "TED"
driver_path = "tools/chromedriver"
num_pagedown = 0

# setup Driver|Chrome : 크롬드라이버를 사용하는 driver 생성
sys.path.append(os.path.dirname(os.path.abspath(driver_path)))
driver = webdriver.Chrome(os.path.abspath(driver_path))

# 유투브 페이지 들어가서 '자막' 필터 된 '세바시' 입력
driver.get("https://www.youtube.com/results?sp=EgQQASgBQgQIARIA&search_query=" + keyword ) # 필터: 동영상+자막

print("--- src/crawling/get_subtitle.py START chromedriver ---")

## Youtube_search 최종
elm = driver.find_element_by_tag_name('html')

for j in range(num_pagedown):
    elm.send_keys(Keys.END)
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
    dataset = df({'Title': title, 'Link': link, 'Play': play_time, 'Channel': channel })

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
    dataset = df({'Title': title, 'Link': link, 'Play': play_time, 'Channel': channel })
    dataset = dataset.loc[dataset['Title'] != ' ',:]

print("--- src/crawling/get_subtitle.py START get subtitle meta ---")

# 영상 URL로 downsub 사이트 들어가서 입력
link2 = []
data = []

y = 'http://downsub.com'
for i in range(len(dataset['Link'])):
    try:
        data = re.sub('https://www.youtube.com/watch\?v\=','', dataset['Link'][i])
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

print("--- src/crawling/get_subtitle.py START get subtitle files ({}) ---".format((num_pagedown+1)*20))

# 자막 다운받기
for i, down in enumerate(srt_down):
    driver.get(down)
    if not i%10:
        print("--- src/crawling/get_subtitle.py     GET subtitle {}/{} ---".format(i+1, (num_pagedown+1)*20))

print("--- src/crawling/get_subtitle.py START save meta data (video, subtitle) ---")

# srt_dataset
date = []
explain = []
link = []
like = []
unlike = []
subscribe = []
hit = []

for i, url in enumerate(dataset['Link']):
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
    like.append(like_soup[0].findAll(text=True)[-1])
    unlike.append(unlike_soup[1].findAll(text=True)[-1])
    subscribe.append(subscribe_soup[0].find(text=True))
    hit.append(hit_soup[0].find(text=True).replace('조회수 ','').replace('회','').replace(',',''))    

    link.append(url)
   
    if not i%10:
        print("--- src/crawling/get_subtitle.py     GET subtitle meta {}/{} ---".format(i+1, (num_pagedown+1)*20))

dataset2 = df({'Link' : link, 'Date' : date, 'Explain' : explain, 'Like' : like, 'Unlike' : unlike, 'Subscribe' : subscribe, 'Hit' : hit})

srt_dataset = pd.merge(dataset,dataset2)

# 저장
srt_dataset.to_csv("srt_dataset.csv")
