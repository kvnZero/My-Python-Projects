#-- coding: utf-8 --
import requests
import json
from datetime import datetime, date
import random
import calendar
from xml.dom.minidom import parse
import xml.dom.minidom
import sys
session = requests.session()

class xixunyun():
    def __init__(self):
        self.session = requests.session()
        self.token = ""
        self.user_id = ""
    def login_xixun(self, classid, password):
        post_data = {"app_version":"3.3.1",
                "registration_id":"170976fa8ab6f764b1d",
                "uuid":"02%3A00%3A00%3A00%3A00%3A00",
                "platform":"2",
                "request_source":"3",
                "password":password,
                "system":"6.0.1",
                "school_id":"34",
                "model":"IPHONE-X",
                "app_id":"cn.vanber.xixunyun.saas",
                "account":classid,
                "key":"y4HK8b3c3sQ0q6DqBwXgglx8NYMAXFW%2B",
        }
        try:
            data = self.session.post("https://api.xixunyun.com/login/api?platform=android&version=3.3.1&token=01c47ce30786a42cc4358c61ff02cf11&entrance_year=0&graduate_year=0",data=post_data,verify=True).text
        except TimeoutError:
            data = ""
        json_data = json.loads(data)
        try:
            self.token = json_data['data']['token']
            self.user_id = json_data['data']['user_id']
        except TypeError:
            return False
        else:
            return True

    def playcard(self, address, latitude, longitude):
        post_data={
            "address":address,
            "latitude":latitude,
            "sign_type":"0",
            "longitude":longitude
        }
        data = self.session.post("https://api.xixunyun.com/signin?platform=android&version=3.3.1&token=%s&entrance_year=0&graduate_year=0" % self.token,data=post_data,verify=True)
        json_data = json.loads(data.text)
        if json_data['code'] == 20000 or json_data['code'] == 64032:
            return True
        else:
            return False
    def write_month(self,strdate,alltext, gettext, questext):
        post_data={"end_date":strdate,
                  "business_type":"month",
                  "content":'[{"content":"%s","require":0,"sort":1,"title":"本月工作总结"},{"content":"%s","require":0,"sort":2,"title":"本月工作成果及收获"},{"content":"%s","require":0,"sort":3,"title":"下月计划安排"}]' % (alltext, gettext, questext),
                  "start_date":strdate}
        data = self.session.post("https://api.xixunyun.com/Reports/StudentOperator?platform=android&version=3.3.1&token=%s&entrance_year=0&graduate_year=0" % self.token,data=post_data, verify=True)
        json_data = json.loads(data.text)
        if json_data['code'] == 20000:
            return True
        else:
            return False
    def write_week(self,strdate, alltext, gettext,nexttext):
        post_data = {"end_date": strdate,
                     "business_type": "week",
                     "content": '[{"content":"%s","require":0,"sort":1,"title":"本周工作总结"},{"content":"%s","require":0,"sort":2,"title":"本周心得体会"},{"content":"%s","require":0,"sort":3,"title":"问题及困难反馈"}]' % (alltext, gettext, nexttext),
                     "start_date": strdate}
        data = self.session.post(
            "https://api.xixunyun.com/Reports/StudentOperator?platform=android&version=3.3.1&token=%s&entrance_year=0&graduate_year=0" % self.token,data=post_data, verify=True)
        json_data = json.loads(data.text)
        if json_data['code'] == 20000:
            return True
        else:
            return False
    def get_weekreport(self):
        self.collection = xml.dom.minidom.parse(sys.path[0]+"/report/report.xml").documentElement
        report_i = self.collection.getElementsByTagName("row")
        typeya = alltext = gettext = questext = ""
        while typeya != "week":
            report = report_i[random.randint(0,len(report_i))]
            typeya = report.getElementsByTagName('type')[0].childNodes[0].data

        alltext = report.getElementsByTagName('list1')[0].childNodes[0].data
        try:
            gettext = report.getElementsByTagName('list2')[0].childNodes[0].data
        except IndexError:
            gettext = "暂无～"

        try:
            questext = report.getElementsByTagName('list3')[0].childNodes[0].data
        except IndexError:
            questext = "暂无～"
        return (alltext,gettext,questext)

    def get_monthreport(self):
        self.collection = xml.dom.minidom.parse(sys.path[0]+"/report/report.xml").documentElement
        report_i = self.collection.getElementsByTagName("row")
        typeya = alltext = gettext = nexttext = ""
        while typeya != "month":
            report = report_i[random.randint(0,len(report_i))]
            typeya = report.getElementsByTagName('type')[0].childNodes[0].data

        alltext = report.getElementsByTagName('list1')[0].childNodes[0].data
        try:
            gettext = report.getElementsByTagName('list2')[0].childNodes[0].data
        except IndexError:
            gettext = "暂无～"

        try:
            nexttext = report.getElementsByTagName('list3')[0].childNodes[0].data
        except IndexError:
            nexttext = "暂无～"
        return (alltext, gettext, nexttext)


    def run(self,lock=False):
        now = datetime.utcnow()
        self.login_xixun("z15f3515", "xusong")
        if self.playcard(address="广东省深圳市龙华区东环一路靠近广发银行", latitude="22.645547", longitude="114.037166") == True:
            firstDayWeekDay, monthRange = calendar.monthrange(now.year, now.month)
            lastday = date(year=now.year, month=now.month, day=monthRange)
            if lastday.day == now.day:
                alltext, gettext, nextext = self.get_monthreport()
                self.write_month("%s/%s/%s" % (now.year, now.month, now.day),alltext,gettext,nextext)
            else:
                if date.weekday(date.today()) == 6:
                    alltext, gettext, questext = self.get_weekreport()
                    self.write_week("%s/%s/%s" % (now.year, now.month, now.day),alltext,gettext,questext)
def xixunyun_playcard():
    _xixunyun = xixunyun()
    _xixunyun.run()

def today_weather(city_id):
    API_KEY = "svbgsoto2mk6fvna"
    USER_ID = "U90560AB9B"
    for city in city_id:
        url = "https://api.seniverse.com/v3/weather/now.json?key=svbgsoto2mk6fvna&location=%s&language=zh-Hans&unit=c" % city
        json_text = json.loads(session.get(url).text)
        temperature = json_text['results'][0]['now']['temperature']
        text = json_text['results'][0]['now']['text']
        address = json_text['results'][0]['location']['name']
        status = ""
        tips = ""
        print("In %s is very %s,and %s, temperature:%s, tips:%s" % (address, status, text, temperature, tips))
def main():
    today_weather(['W7VHZEYSJ2W6'])
    xixunyun_playcard()

if __name__ == "__main__":
    main()