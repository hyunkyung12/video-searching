from flask import Flask, request, jsonify
from flask import render_template
import json
import os
import pandas as pd
import numpy as np
import csv
from find_exec_target import exec_find, target_find, upload_check_list

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return(render_template("prac.html"))

@app.route('/recommend', methods=['GET', 'POST'])

def recommend(): # button 에 적용될 function 이름
    rst = "replay"
    if request.method == 'POST':
        try:
            demo = pd.read_csv("./data/kor_sub.csv")
            inputStory =  request.form['myStory']; #myStory : params 이름
            rst = target_find(inputStory)
        except Exception as e:
            print(e)
    
    rtn = upload_check_list()
    return rtn

if __name__ == "__main__":
	#upload_data()
	app.run()