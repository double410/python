from flask import jsonify
from app import app
from bson import json_util
import json
import pymongo
from pymongo import MongoClient
import datetime


@app.route('/api/v1.0/homeworks', methods=['GET'])
def get_homeworks():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    s_date = str(now.month) + "/"  + str(now.day) + "/" + str(now.year)
    
    # s_date = request.form['selected_date']
    # start = datetime.datetime.strptime(s_date, "%m/%d/%Y")

    next_day = start + datetime.timedelta(days=1)
   
    client = MongoClient('localhost', 27017)
    homework  = client.test.homeworks.find_one({"date": {"$lt": next_day, "$gte": start}})

    if not homework:
        homework = client.test.homeworks.find().sort("date", pymongo.DESCENDING).limit(1)[0]
        
    return json_util.dumps(homework, ensure_ascii=False, indent=2)
