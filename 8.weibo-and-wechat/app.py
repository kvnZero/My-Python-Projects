#coding=utf8
import itchat
from itchat.content import TEXT
import requests
import re
import base64
import json
import binascii
import rsa
import os
from PIL import Image


class Weibo():
    def __init__(self, username, password):
        self.session = requests.session()
        self.username = username
        self.password = password
        self.uid = ""
        self.pcid = ""
    def userLogin(self, pagecount=1):
        #login weibo.com
        self.Header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        url_prelogin = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client='
        url_login = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
        resp = self.session.get(url_prelogin, headers=self.Header)
        json_data = re.findall(r'(?<=\().*(?=\))', resp.text)[0]
        data = json.loads(json_data)
        servertime = data['servertime']
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        su = base64.b64encode(self.username.encode(encoding="utf-8"))
        rsapublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsapublickey,65537)
        message = str(servertime)+'\t'+str(nonce)+'\n'+str(self.password)
        sp = binascii.b2a_hex(rsa.encrypt(message.encode(encoding="utf-8"), key))
        postdata = {
            'entry':'weibo',
            'gateway':'1',
            'from':'',
            'savestate':'7',
            'userticket':'1',
            'ssosimplelogin':'1',
            'vsnf':'1',
            'vsnval':'',
            'su':su,
            'service':'miniblog',
            'servertime':servertime,
            'nonce':nonce,
            'pwencode':'rsa2',
            'sp':sp,
            'encoding':'UTF-8',
            'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype':'META',
            'rsakv':rsakv,
            }
        if self.code != "" and self.pcid != "":
            postdata['pcid'] = self.pcid
            postdata['door'] = self.code
        resp=self.session.post(url_login,data=postdata,headers=self.Header)
        login_url=re.findall(r'http://weibo.*&retcode=0', resp.text)
        try:
            respo = self.session.get(login_url[0], headers=self.Header)
            uid = re.findall('"uniqueid":"(\d+)",', respo.text)[0]
            self.uid = uid
            url = "http://weibo.com/u/" + uid
            respo = self.session.get(url, headers=self.Header).text
            print("login success: uid[%s]" %uid)
        except IndexError:
            print("login error: code or other error")
            os._exit(0)
    def getCode(self):
        self.Header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        su = base64.b64encode(self.username.encode(encoding="utf-8"))
        get_code_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1502779202863" % su.decode("utf-8")
        data_txt = self.session.get(get_code_url, headers = self.Header).text
        showpin_re = re.findall(r'showpin":(.+?),', data_txt)
        showpin = showpin_re[0]
        if showpin == "1":
            pcid_re = re.findall(r'"pcid":"(.+?)"', data_txt)
            return pcid_re[0]
        else:
            return 0
    def getCodeImage(self, pcid):
        self.Header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.pcid = pcid
        image = self.session.get("https://login.sina.com.cn/cgi/pin.php?r=62210336&s=0&p=" + pcid,headers = self.Header).content
        return image
    def setCode(self, code):
        self.code = code
    def run(self):
        pass

if __name__ == "__main__":
    username = input("Username:")
    password = input("Password:")
    weibo = Weibo(username, password)
    iscode = weibo.getCode()
    if iscode != 0:
        print("login need code")
        with open("code.png", "wb") as file:
            file.write(weibo.getCodeImage(iscode))
        code_image = Image.open("code.png").show()
        code = input("Code :")
        weibo.setCode(code)
    weibo.userLogin()
    itchat.auto_login()
    itchat.run(blockThread=False)
    while True:
        weibo.run()