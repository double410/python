from selenium import webdriver
import json
from json import JSONEncoder
import pymongo
from pymongo import MongoClient
import datetime


class DocHomework:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.test
        self.homeworks = self.db.homeworks

    def upsert_homework(self, date, homework):
        next_day = date + datetime.timedelta(days=1)
        self.homeworks.update({"date": {"$lt": next_day, "$gte": date}}, homework, True)

    def query_homework(self, date):
        delta = datetime.timedelta(days=1)
        next_day = date + delta
        hw = self.homeworks.find_one({"date": {"$lt": next_day, "$gte": date}})
        return hw

    def get_latest_homework(self):
        lst_hw = self.homeworks.find().sort("date", pymongo.DESCENDING).limit(1)
        if lst_hw:
            hw = lst_hw[0]
        return hw


class WebHomework:

    def __init__(self, url, user_name, password):
        self.url = url
        self.user_name = user_name
        self.password = password

    def get_homework(self):
        homework = {}

        browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        browser.get(self.url)

        browser.find_element_by_id("login_tbxUserName").send_keys(self.user_name)
        browser.find_element_by_id("login_tbxPassword").send_keys(self.password)
        browser.find_element_by_id("login_btnlogin").click()

        browser.find_element_by_name("Image14").click()
        mymsg = browser.find_element_by_id("MyMSG").text
        homework["title"] = mymsg

        list_td = browser.find_elements_by_tag_name("td")
        classes = []
        for td in list_td:
            if td.get_attribute("BGCOLOR") == "#E2E4FA":
                cls = {}
                cls["subject"] = td.text
            elif (td.get_attribute("align") == "left" and td.get_attribute("valign") == "top"):
                if not td.get_attribute("style"):
                    cls["content"] = td.text
                    classes.append(cls)
        homework["classes"] = classes
        browser.quit()
        s = json.dumps(homework, ensure_ascii=False, indent=2)
        return s


class MyEncoder(JSONEncoder):
    def defaut(self, o):
        return o.__dict__

def set_homework():
    web_homework = WebHomework("http://www.fushanedu.cn/jxq/jxq.aspx", "20162424", "xjamma(1314)")
    homework = json.loads(web_homework.get_homework())
    now = datetime.datetime.now()
    homework["date"] = now

    start = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    doc = DocHomework()

    doc.upsert_homework(start, homework)

set_homework()
