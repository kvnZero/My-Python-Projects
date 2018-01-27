import requests
import re
import sys
import os

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
            result = re.findall(r'<span class="red">([0-9]+)</span>',result_text)
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
            if not os.path.exists("images"):
                os.makedirs("images")
            for url_n in self.images:
                image = self.session.get(url_n).content
                with open("images/%d.jpg" % self.num, "wb") as file:
                    file.write(image)
                self.num += 1
        return self.num

    def download_number(self):
        return self.num

    def save_images_url(self):
        if len(self.images) == 0:
            return False
        url_text = ""
        for url in self.images:
            url_text += url
        with open("image_url.txt","a") as file:
            file.write(url_text + "\n")
        return True

def main():
    try:
        url = sys.argv[1]
    except IndexError:
        print("input tieba url")
        return False
    tieba = Tieba()
    maxpage = tieba.set_tieba_url(url)
    if maxpage == 0:
        print ("error url")
    else:
        print ("maxpage: %s" % maxpage)
        print ("is get images url,waiting...")
        tieba.get_tieba_images()
        print ("images is: %s" % tieba.get_images_number())
        choose = input ("doing(1:download images, 2:save url):")
        if choose == "1":
            print("now is download images, waiting...")
            tieba.download_images()
            print("download %s images" % tieba.download_number())
        else:
            if tieba.save_images_url():
                print("save in :image_url")
            else:
                print("not images")

            #write save code

if __name__ == '__main__':
    main()
