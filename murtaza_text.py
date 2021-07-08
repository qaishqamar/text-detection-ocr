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

    pytesseract.tesseract_cmd='C:\\Users\\qamar\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
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
                    print(b)
                    if len(b)==12:
                        x,y,w,h=int(b[6]),int(b[7]),int(b[8]),int(b[9])
                        cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),1)
                        cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2) 
                        # if char(cv2.waitKey(0))=='n':
                            
        ####### detecting words ############
        boxes=pytesseract.image_to_data(img)
        draw_box(boxes)
        text=pytesseract.image_to_string(img)
        ## thread_speaker function by creating new thread ######
        x=threading.Thread(target=thread_speaker,args=(text,))
        x.start()
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20,230,20), 2);
        cv2.imshow("Result",img)
        if cv2.waitKey(0)==62:   # for capturing next image by pressing right arrow #
            continue
        if cv2.waitKey(0)==13:   # for breaking while by pressing enter #
            break
    cap.release()
    cv2.destroyAllWindows()    



extract_text()
# cv2.imshow('result',img)
# cv2.waitKey(0)