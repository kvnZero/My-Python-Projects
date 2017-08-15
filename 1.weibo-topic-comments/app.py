#coding=utf8
import requests
import base64
import re
import json
import binascii
import rsa
import time
import os
from PIL import Image


def find_mid(mid):
    with open("mid.txt") as file :
        for mids in file.readlines():
            if(mids.strip().lstrip() == mid):
                return True
    return False
def write_mid (mid):
    with open("mid.txt","a") as file :
        file.write(mid+"\n")
class weibo:

    def __init__(self, username, password):
        self.session = requests.session()
        self.username = username
        self.password = password
        self.uid = ""
        self.pcid = ""
        self.code = ""
    def get_code_image(self, pcid):
        get_Header = {
                      "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
                      }
        self.pcid = pcid
        image = self.session.get("https://login.sina.com.cn/cgi/pin.php?r=62210336&s=0&p=" + pcid,headers = get_Header).content
        return image
    def get_code(self):
        get_Header = {
                      "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
                      }
        su = base64.b64encode(self.username.encode(encoding="utf-8"))
        get_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1502779202863" % su.decode("utf-8")
        date_txt = self.session.get(get_url,headers = get_Header).text
        showpin_re = re.findall(r'showpin":(.+?),',date_txt)
        showpin = showpin_re[0]
        if showpin == "1":
            pcid_re = re.findall(r'"pcid":"(.+?)"',date_txt)
            return pcid_re[0]
        else:
            return 0
    def set_code(self, code):
        self.code = code
    def user_login(self, pagecount=1):
        #登录微博
        get_Header = {
                      "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
                      }
        url_prelogin='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client='
        url_login='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
        resp=self.session.get(url_prelogin,headers=get_Header)
        json_data=re.findall(r'(?<=\().*(?=\))',resp.text)[0]
        data=json.loads(json_data)
        servertime=data['servertime']
        nonce=data['nonce']
        pubkey=data['pubkey']
        rsakv=data['rsakv']
        su=base64.b64encode(self.username.encode(encoding="utf-8"))
        rsapublickey=int(pubkey,16)
        key=rsa.PublicKey(rsapublickey,65537)
        message=str(servertime)+'\t'+str(nonce)+'\n'+str(self.password)
        sp=binascii.b2a_hex(rsa.encrypt(message.encode(encoding="utf-8"),key))
        postdata={
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
        if self.code !="" and self.pcid !="" :
            postdata['pcid'] = self.pcid
            postdata['door'] = self.code
        resp=self.session.post(url_login,data=postdata,headers=get_Header)
        login_url=re.findall(r'http://weibo.*&retcode=0',resp.text)
        try:
            respo = self.session.get(login_url[0],headers=get_Header)
            uid = re.findall('"uniqueid":"(\d+)",', respo.text)[0]
            self.uid=uid
            url = "http://weibo.com/u/" + uid
            respo = self.session.get(url,headers=get_Header).text
            print ("登录成功 uid:%s" %uid)
        except IndexError:
            print ("登录失败\n验证码错误或其他原因")
            os._exit(0)
    def run_good(self, topic_id, content= "[抱抱]", run_time= 10):
        url = "http://weibo.com/p/%s/super_index" % topic_id
        get_Header ={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Host":"weibo.com",
            "Proxy-Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }
        while True:
            data = self.session.get(url,headers=get_Header).text
            return_re = re.findall(r'<script>FM.view(.+?)</script>', data)
            return_txt = return_re[-1]
            return_txt = return_txt[1:-1]
            html_json = json.loads(return_txt)
            try:
                html = html_json['html']
                return_re = re.findall(r'value=pubuser_head:(\d+)\"', str(html))
                for mid in return_re:
                    if find_mid(mid) == True:
                        print ("跳过回复：%s" % mid)
                        continue
                    post_Url = "http://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd=1502505345628"
                    post_Header = {"Accept":"*/*",
                                "Accept-Encoding":"gzip, deflate",
                                "Accept-Language":"zh-CN,zh;q=0.8",
                                "Connection":"keep-alive",
                                "Content-Length":"230",
                                "Content-Type":"application/x-www-form-urlencoded",
                                "Host":"weibo.com",
                                "Origin":"http://weibo.com",
                                "Referer":url,
                                "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
                                "X-Requested-With":"XMLHttpRequest"
                               }
                    post_Data =  {
                        "act":"post",
                        "mid":mid,
                        "uid":self.uid,
                        "forward":"0",
                        "isroot":"0",
                        "content":content,
                        "location":"page_100808_super_index",
                        "module":"scommlist",
                        "group_source":"filter_actionlog:",
                        "pdetail":topic_id,
                        "_t":"0",
                    }
                    return_json =  self.session.post(post_Url,post_Data,headers=post_Header).text
                    data = json.loads (return_json)
                    if data['code']=="100000":
                        print ("已经回复：" + mid)
                        write_mid(mid)
                    else:
                        print ("回复失败:" + data['msg'])
                    time.sleep(5)
            except KeyError:
                print ("访问错误")
            time.sleep(run_time)

if __name__ == "__main__":
    username = input("Username:")
    password = input("Password:")
    ouhuang = weibo(username,password)
    iscode = ouhuang.get_code()
    if iscode != 0:
        with open("code.png","wb") as file:
            file.write (ouhuang.get_code_image(iscode))
        code_image = Image.open("code.png").show()
        code = input("Code :")
        ouhuang.set_code(code)
    ouhuang.user_login()
    topic_id = input("Topic_ID :")
    content = input("Content([抱抱]):")
    runtime = input("Runtime(60):")
    if runtime == "":
        runtime = 60
    if content == "":
        content = "[抱抱]"
    ouhuang.run_good(topic_id,content,int(runtime))
