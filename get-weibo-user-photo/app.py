import requests
import re 
import random
import time
import os

def get_cookies():
    r = session.get("https://weibo.com/", allow_redirects=False)
    Ugrow_G0 = r.cookies['Ugrow-G0']
    LoginURL = r.headers.get('Location')
    LoginCookie = session.get(LoginURL).cookies['login']
    GenURL = "https://passport.weibo.com/visitor/genvisitor"
    Payload = {'cb': 'gen_callback',
                'fp': {"os": "1", "browser": "Gecko65,0,0,0", "fonts": "undefined", "screenInfo": "1920*1080*24","plugins": ""}}
    r = session.post(GenURL, data=Payload, cookies=dict(login=LoginCookie))
    tid = re.search(r'(?<="tid":").*?(?=")', r.text).group(0)
    LoginURL = "https://passport.weibo.com/visitor/visitor?"
    Payload = {'a': 'incarnate', 't': tid, 'w': '3', 'c': '100', 'gc': '',
                'cb': 'cross_domain', 'from': 'weibo', '_rand': str(random.uniform(0, 1))+str(random.uniform(999, 10000))}
    r = session.get(LoginURL, params=Payload, cookies=dict(login=LoginCookie, tid=tid+"__100"))
    try:
        sub = r.cookies['SUB']
        subp = r.cookies['SUBP']
        return dict(Ugrow_G0=Ugrow_G0, SUB=sub,  SUBP=subp)
    except KeyError:
        return {}

def download(imglist, dirname=""):
    if not dirname:
        dirname = str(int(time.time()))
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    for url in imglist:
        filename = re.findall(r'(large/(.*?).jpg)', url)[0][1]
        print("download:%s" % filename)
        with open("%s/%s.jpg" % (dirname, filename), mode='wb') as file:
            file.write(session.get(url).content)

def getImage(uid):
    #访客接口只能浏览一页
    url = "https://weibo.com/p/%s/photos?type=photo" % uid

    #登录后接口（简化） 可以进行翻页
    #https://weibo.com/p/aj/album/loading?ajwvr=6&type=photo&owner_uid=20000&viewer_uid=20000&page_id=1005051868515735&page=2&ajax_call=1&since_id=4400509448638030_4367496142061900_20190819_-1

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }
    resp = session.get(url, headers = headers)
    pageHtml = re.findall(r'(?<=\().*(?=\))', resp.text)
    urllist = re.findall(r'(mw1024%2F(.*?).jpg)', pageHtml[len(pageHtml)-1])
    imglist = []
    for url in urllist:
        imglist.append("http://wx2.sinaimg.cn/large/%s.jpg" % url[1])
        #原图地址
    return (imglist) 

if __name__ == "__main__":
    cookies = {}
    i=1
    while not cookies:
        print("第%i次尝试获取访客状态" % i)
        session = requests.session()
        cookies = get_cookies()
        if cookies:
            print("获取成功将获取照片墙")
        else:
            i=i+1
    uid = "" #需要获取的微博Uid
    download(getImage(uid),uid)
