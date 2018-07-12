# Video Search

### 날 따라 해봐요 (180713)
1. `python src/crawling/get_subtitle.py keyword`
	keyword에는 검색할 단어(혹은 문장)가 들어가야 함!
2. `python src/preprocessing/cleansing_subtitle.py`

참고로 DB가 계속 누적되는 형식이므로, 뭐가 잘못되서 처음부터 하고 싶으면 아래를 한번 해줘야함
`python src/db/init_db.py`

### git 으로 협업하기

1. git clone https://github.com/hyunkyung12/video-searching.git
2. git checkout -b (branch 이름)
3. git add (수정내용)
4. git commit -m (메시지)
5. git push origin (branch 이름)
6. 다른 사람의 내용을 적용하려면 git pull origin (branch 이름)

### 회의 내용

##### 0527 회의

전체 process

![](./history/0527.png)

##### 0603 회의