from flask import Flask, request, jsonify
from flask import render_template
import json
import os
import pandas as pd
import numpy as np
import csv
#from find_exec_target import iter_in_s, exec_find, exec_words_find, target_find, write_json, read_json, make_new_json
#import sys
#sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/search/get_jaccard_result.py')
import get_jaccard_result

file_name = sys.argv[1] # 어떤 자막파일?
#sentence = sys.argv[2]
num = sys.argv[2] # list 몇개?

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return(render_template("prac.html"))

@app.route('/recommend', methods=['GET', 'POST'])
def recommend(file_name, num): # button 에 적용될 function 이름
    #render_template("prac.html")
    rst = "replay"
    if request.method == 'POST':
        try:
            #demo = pd.read_csv("./data/kor_sub.csv")
            inputStory =  request.form['myStory']; #myStory : params 이름
            rst = compare_subtitle_kkma(inputStory, file_name, num)
            #rst = target_find(inputStory)
        except Exception as e:
            print(e)
    rtn = make_new_json()
    return rtn

if __name__ == "__main__":
	#upload_data()
	app.run()