from selenium import webdriver
import json
from json import JSONEncoder


class Course:
    
    def __init__(self):
        self.subject = ""
        self.content = ""

    def set_subject(self, subject):
        self.subject = subject
 
    def set_content(self, content):
        self.content = content

    def get_subject(self):
        return self.subject

    def get_content(self):
        return self.content

    def __repr__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

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

        return homework


class MyEncoder(JSONEncoder):
    def defaut(self, o):
        return o.__dict__

homework = WebHomework("http://www.fushanedu.cn/jxq/jxq.aspx", "20162424", "xjamma(1314)")
list_hw = homework.get_homework()

out = open("/home/Fred/han/data/homework.json", mode="w", encoding="utf-8")
out.write(json.dumps(list_hw, cls=MyEncoder, ensure_ascii=False, indent=2))
out.close()
