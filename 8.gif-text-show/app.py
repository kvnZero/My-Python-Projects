#coding:utf8
from PIL import Image,ImageSequence
import os
from time import sleep
class Ptrancefrom(object):
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

    def git_to_png(self,image):
        with Image.open(image) as im:
            if im.is_animated:  #判断是否为动态
                pngfilelist = list()
                i = 0
                for f in ImageSequence.Iterator(im):
                    f.save("pngfile_%s.png" % i)
                    pngfilelist.append("pngfile_%s.png" % i) 
                    i += 1
                                       
        return pngfilelist


    def get_char(self, r, b, g, alpha = 256):
        if alpha == 0:
            return ' '
        length = len(self.ascii_char)
        gray = int(0.2126*r+ 0.7152*g+ 0.0722*b)
        unit = (256.0 + 1) / length
        return self.ascii_char[int(gray/unit)]

    def print_picture(self, img):
        im = Image.open(img)
        im = im.convert('RGB') #maybe need this code
        txt = ""
        im = im.resize((self.width,self.heigth), Image.NEAREST)
        for i in range(self.heigth):
            for j in range(self.width):
                txt += self.get_char(*im.getpixel((j,i)))
            txt += '\n'
        print (txt)

    def play_gif(self, pngfilelist):
        for pngfile in pngfilelist:
            sleep(1)
            os.system('cls')
            self.print_picture(pngfile)
            os.remove(pngfile)

if __name__ == "__main__":
    pic = Ptrancefrom(60,30)
    pngfilelist = pic.git_to_png("t01522b4b16b103aee9.gif")
    pic.play_gif(pngfilelist)
