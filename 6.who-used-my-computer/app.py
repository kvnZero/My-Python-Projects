# -*- coding: utf-8 -*-
import cv2
import time

def SaveVideoImage():
    cap = cv2.VideoCapture(0) # if 0 not images ,try 1, 2 or more(usually 0~2)
    ok, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    # if need have face then save images you can write get face code ~
    timenow = time.time()
    cv2.imwrite("image%s.jpg" % timenow,frame)

if __name__ == '__main__':
    number = 0
    while True:
        SaveVideoImage()
        number = number + 1
        if number == 3:
            exit()
        time.sleep(10)