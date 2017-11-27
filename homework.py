from selenium import webdriver
#from wechat_sdk import WechatConf
#from wechat_sdk import WechatBasic

class WebHomework:
    def __init__(self, url, user_name, password):
        self.url = url
        self.user_name = user_name
        self.password = password
    
    def get_homework(self):
        homework = []

        browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        browser.get(self.url)
        
        browser.find_element_by_id("login_tbxUserName").send_keys(self.user_name)
        browser.find_element_by_id("login_tbxPassword").send_keys(self.password)
        browser.find_element_by_id("login_btnlogin").click()

        browser.find_element_by_name("Image14").click()
        mymsg = browser.find_element_by_id("MyMSG").text
        homework.append("<h2>"+mymsg+"</h2>")

        list_td = browser.find_elements_by_tag_name("td")
        for td in list_td:
            if td.get_attribute("BGCOLOR") == "#E2E4FA":
                homework.append("<h3>"+td.text+"</h3>")
            elif (td.get_attribute("align") == "left" and td.get_attribute("valign") == "top"):
                if not td.get_attribute("style"):
                    homework.append("<p class=\"lead\">"+td.text+"</p>")

        browser.quit()

        return homework
 
homework = WebHomework("http://www.fushanedu.cn/jxq/jxq.aspx", "xxxxxx", "xxxxxxx")

out = open("/home/Fred/han/index.html", "w")

out.write("<html><head>")
out.write("<META http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">")
out.write("<link rel=\"stylesheet\" href=\"//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css\">")
out.write("</head>")
out.write("<body><div>")

for item in homework.get_homework():
    out.write("\n")
    out.write(item)

out.write("</div></body></html>")

out.close()
