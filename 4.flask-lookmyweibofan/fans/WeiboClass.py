import requests, re, base64, json, binascii, rsa
from bs4 import BeautifulSoup

class Weibo():
    def __init__(self, username, password):
        print("Weclome to use Weibo.Class")
        self.uid = ""
        self.username = username
        self.password = password
        self.pcid = ""
        self.code = ""
        self.session = requests.session()

    def checkCode(self):
        '''
        Check username need input code
        if return 0 is not input code
        else use getCode()
        '''
        Header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        su = base64.b64encode(self.username.encode(encoding="utf-8"))
        get_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1502779202863" % su.decode("utf-8")
        data_txt = self.session.get(get_url,headers = Header).text
        showpin_re = re.findall(r'"showpin":[0|1]', data_txt)
        if showpin_re[0] == '"showpin":0':
            pcid_re = re.findall(r'"pcid":"(.+?)"', data_txt)
            self.pcid = pcid_re[0]

    def getCode(self):
        '''
        if use this function befor not use checkCode is return error
        :return code image use PIL or other open image function:
        '''

        if self.pcid == "":
            raise ValueError('pcid is empty, if has been use "checkCode", use "loginWeibo" else use "checkCode"')

        Header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        image = self.session.get("https://login.sina.com.cn/cgi/pin.php?r=62210336&s=0&p=" + self.pcid,headers = Header).content
        return image

    def loginWeibo(self):
        '''
        Use This function befor use checkCode
        :return uid or 0:
        '''

        Header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        url_prelogin = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client='
        url_login = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
        resp = self.session.get(url_prelogin, headers=Header)
        json_data = re.findall(r'(?<=\().*(?=\))', resp.text)[0]
        data = json.loads(json_data)
        servertime = data['servertime']
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        su = base64.b64encode(self.username.encode(encoding="utf-8"))
        rsapublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsapublickey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password)
        sp = binascii.b2a_hex(rsa.encrypt(message.encode(encoding="utf-8"), key))
        postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'ssosimplelogin': '1',
            'vsnf': '1',
            'vsnval': '',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'sp': sp,
            'encoding': 'UTF-8',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
            'rsakv': rsakv,
        }
        if self.code != "" and self.pcid != "":
            postdata['pcid'] = self.pcid
            postdata['door'] = self.code
        resp = self.session.post(url_login, data=postdata, headers=Header)
        login_url = re.findall(r'http://weibo.*&retcode=0', resp.text)
        try:
            respo = self.session.get(login_url[0], headers=Header)
            uid = re.findall('"uniqueid":"(\d+)",', respo.text)[0]
            self.uid = uid
            url = "http://weibo.com/u/" + uid
            return uid
        except IndexError:
            return 0

    def getFans(self):
        '''
        use this function get you fans
        then you can use "showFans" show you fans
        :return fans number:
        '''

        if self.uid == "":
            raise ValueError('you need login after use this function.')

        get_url = "http://weibo.com/%s/fans?pids=Pl_Official_RelationFans__88&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__88_page=0&ajaxpagelet=1&ajaxpagelet_v6=1" % self.uid
        Headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding":"gzip, deflate, sdch",
                   "Accept-Language":"zh-CN,zh;q=0.8",
                   "Connection":"keep-alive",
                   "Host":"weibo.com",
                   "Referer":"http://weibo.com/%s/fans?cfs=600&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__88_page=3" % self.uid,
                   "Upgrade-Insecure-Requests":"1",
                   "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        #maxpage = int(re.findall(r'Pl_Official_RelationFans__88_page=(.+?)#',self.session.get(get_url,headers=Headers).text)[-2])
        maxpage=1
        users_data={}
        for page in range(1, maxpage + 1):
            get_url = "http://weibo.com/%s/fans?pids=Pl_Official_RelationFans__88&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__88_page=%i&ajaxpagelet=1&ajaxpagelet_v6=1" % (self.uid,page)
            data_json = json.loads(re.findall(r'view\((.*)\)', self.session.get(get_url, headers=Headers).text)[0])
            soup = BeautifulSoup(data_json['html'], "html.parser")
            for users in soup.find_all("dd", class_="mod_info S_line1"):
                a = str(users.find_all("a"))
                username = re.findall(r'title="(.+?)"', a)[0]
                userid = re.findall(r'id=(.+?)&', a)[0]
                follow = re.findall(r'>(.+?)</a>', a)[2]
                fans = re.findall(r'>(.+?)</a>', a)[3]
                weibo = re.findall(r'>(.+?)</a>', a)[4]
                address = str(users.find("div", class_="info_add").text)[2:]
                byfrom = str(users.find("a", class_="S_link2").text)

    def showFans(self, **kwargs):
        '''
        choose: address, follow, fans, weibo, byfrom
        you can like this input:
            address = "其他"
            follow = 100 (this show >=100 user)
            fans = 100 (this show >=100 user)
            weibo = 5 (this show >=5 user)
            byfrom = "微博推荐"
        :return list:
        '''


if __name__ == "__main__":
    weibo = Weibo("13516673902","llkilwj")
    weibo.loginWeibo()
    weibo.getFans()
