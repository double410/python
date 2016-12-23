from flask import render_template, request
from app import app
import pymongo
from pymongo import MongoClient
import datetime
import json

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    s_date = str(now.month) + "/"  + str(now.day) + "/" + str(now.year)
    message = {"is_hidden": "hidden", "msg": ""}
    
    if request.method == 'POST':
        s_date = request.form['selected_date']
        start = datetime.datetime.strptime(s_date, "%m/%d/%Y")

    next_day = start + datetime.timedelta(days=1)
   
    client = MongoClient('localhost', 27017)
    homework  = client.test.homeworks.find_one({"date": {"$lt": next_day, "$gte": start}})

    if not homework:
        homework = client.test.homeworks.find().sort("date", pymongo.DESCENDING).limit(1)[0]
        message["msg"] = "当天没有作业记录！"
        message["is_hidden"] = ""

    return render_template("index.html", homework = homework, selected_date = s_date, message = message)
