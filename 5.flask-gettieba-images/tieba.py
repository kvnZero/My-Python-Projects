import requests
import re

class Tieba():
    def __init__(self):
        print ("Welcome to use get tieba images")
        self.session = requests.session()
        self.maxpage = 0
        self.num = 0
        self.images = []
        self.url = ""

    def set_tieba_url(self, url):
        '''
            if return 0 :error url
            else return maxpage
        '''
        ruls = r'(http|https)://tieba.baidu.com/p/([0-9]*)'
        result = re.findall(ruls, url)
        if len(result) == 0:
            self.maxpage = 0
        else:
            self.url = url
            result_text = self.session.get(self.url).text
            result = re.findall(r'<span class="red">([0-9])</span>页</li>',result_text)
            self.maxpage = result[0]
        return self.maxpage

    def get_tieba_images(self):

        if self.maxpage == 0:
            return ""

        for i in range(1, int(self.maxpage) + 1):
            url = "%s?pn=%d" % (self.url, i)
            result_text = self.session.get(url).text
            ruls = r'https://imgsa.baidu.com/forum/w%3D580/sign=(.+?).jpg'
            result = re.findall(ruls, result_text)
            for url_n in result:
                self.images.append('https://imgsa.baidu.com/forum/w%3D580/sign='+url_n+'.jpg')

    def get_images_number(self):
        return len(self.images)

    def download_images(self):
        self.num = 1
        if len(self.images) == 0:
            return self.num
        else:
            for url_n in self.images):
                image = self.session.get(url).content
                with open("images/%d.jpg" % self.num, "rb") as file:
                    file.write(image)
                self.num += 1
        return self.num

    def download_number(self):
        return self.num
