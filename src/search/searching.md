1. get_morphs.py (형태소 분석 결과를 data/morphs.csv로 저장)
``
$python get_morphs.py inputfile_name
``
- input file 은 data folder안에 들어있어야함
- input file의 col명은 subtitle_file.csv(demo)와 같아야함


2. get_jaccard_result.py (자카드 결과 data/jaccard_checklist.csv로 저장)
``
$python get_jaccard_result.py filename(morphs고정) input_sentence output_num
``
- get_morphs.py 수행후 돌려야함
- 첫번째 인자 morphs(1번의 결과)로 고정
- 두번째, 세번째 인자값 입력
- output_num 결과값의 개수

3. w2c_sentence_embedding.py (w2v sentence embedding 결과 /data/morphs_vec.csv로 저장)
``
$python w2c_sentence_embedding.py 
``
4. get_w2v_result.py (w2v 결과 data/w2v_checklist.csv로 저장)
``
$python get_w2v_result.py filename(morphs_vec고정) sentence tokenizing 유사도 num
``
- 1번과 3번 수행후 돌려야함
- 첫번째 인자 morphs_vec(3번의 결과)로 고정
- 두번째 인자 검색할 sentence
- 세번째 인자 : refined(명사 동사만 뽑기) full(다 쓰기) 그외(full로 봄)
- 네번째 인자 : ucli cosine man 그외(man으로 봄)
- 다섯번째 인자 : output 개수
