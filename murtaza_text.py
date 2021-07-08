import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
import time
import pyttsx3
import threading



##############################################
##### Webcam and Screen Capture Example ######
##############################################
#--- for using pc camera
# cap = cv2.VideoCapture(0)


def thread_speaker(text):
    speaker=pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()


def extract_text():
    ## set path to your allready installed pytesseract ocr.exe ##
    pytesseract.tesseract_cmd='C:\\Users\\qamar\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
    ## use 0 as parameter in videoCapture for using pc camera ##
    ## else use a application Ip webcame and paste ip address ##
    ## to use mobile camera ##
    cap = cv2.VideoCapture('http://192.168.43.1:8080/video')
    cap.set(3,640)
    cap.set(4,480)
  
    while True:
        timer = cv2.getTickCount()
        _,img = cap.read()
        #img = captureScreen()
        def draw_box(boxes):
            for x,b in enumerate(boxes.splitlines()):
                if x!=0:
                    b=b.split()  
                    # print(b)
                    if len(b)==12:
                        x,y,w,h=int(b[6]),int(b[7]),int(b[8]),int(b[9])
                        cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),1)
                        cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2) 
                        # if char(cv2.waitKey(0))=='n':
                            
        ####### detecting words ############
        boxes=pytesseract.image_to_data(img)
        text=pytesseract.image_to_string(img)
        if text==None or boxes==None:
            print("capture next frame")
            break
        draw_box(boxes)
        ## thread_speaker function by creating new thread ######
        x=threading.Thread(target=thread_speaker,args=(text,))
        x.start()
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20,230,20), 2);
        cv2.imshow("Result",img)
        res=cv2.waitKey(0) 
        if res==62 or res==78 or res==110 : # for capturing next image 
            print("capture next frame")     # by pressing right shift ot n or N #
            continue
        if res==13: 
            print("close")    # for breaking while by pressing enter #
            break
    cap.release()
    cv2.destroyAllWindows()    



extract_text()
# cv2.imshow('result',img)
# cv2.waitKey(0)