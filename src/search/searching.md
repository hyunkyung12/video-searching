1. get_morphs.py (형태소 분석 결과를 data/morphs.csv로 저장)
``
$python get_morphs.py inputfile_name
``
- input file 은 data folder안에 들어있어야함
- input file의 col명은 subtitle_file.csv(demo)와 같아야함


2. get_J_result.py (자카드 결과 data/J_checklist.csv로 저장)
``
$python get_J_result.py filename(morphs) input_sentence output_num
``
- get_morphs.py 수행후 돌려야함
- 첫번째 인자 morphs 고정
- 두번째, 세번째 인자값 입력
- output_num 결과값의 개수

3. w2c_sentence_embedding.py (w2v sentence embedding 결과 /data/morphs_vec.csv로 저장)
``
$python w2c_sentence_embedding.py 
``
