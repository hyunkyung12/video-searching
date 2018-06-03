## *find_exec_target.py*


####1. 실행 방법:
````
$ python3 find_exec_target.py data func word
````

data : csv 파일명 예) kor_sub.csb -> kor_sub
fucn : exec_find
word : 검색할 단어 입력

####2. 결과: 
check_list.csv 파일이 생성됨
위 파일은 검색한 단어를 포함하는 

| url | start | end |
|--------|--------|---------|
|    string    |    string    |		string	|
를 가지고 있음

- - -
## mv_to_point.py


####1. 실행방법:
find_exec_target.py
를 먼저 실행 시켜야함
(data folder에 check_list.csv 파일 생성된 상태에서 실행 )

```
k=1
```
에 이동하고 싶은 point의 index 번호를 넣어줌

####2. 결과:
셀레늄으로 해당 영상의 start point로 넘어감