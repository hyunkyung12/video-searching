## *find_a_word_in_corpus.py*


####1. 실행 방법:
````
word = '' 
````
부분에 검색할 단어 입력
(단어는 띄어쓰기를 포함하지 않아야함)

####2. 결과: 
result.csv 파일이 생성됨
위 파일은 검색한 단어를 포함하는 

| url | start | end |
|--------|--------|---------|
|    string    |    string    |		string	|
를 가지고 있음



- - -
## mv_to_point.py


####1. 실행방법:
find_a_word_in_corpus.py
를 먼저 실행 시켜야함
(현재 directory에 result.csv 파일 생성된 상태에서 실행 )

```
k=1
```
에 이동하고 싶은 point의 index 번호를 넣어줌

####2. 결과:
셀레늄으로 해당 영상의 start point로 넘어감