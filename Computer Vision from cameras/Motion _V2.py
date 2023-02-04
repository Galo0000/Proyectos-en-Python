import cv2 as cv
import os
import imutils
import numpy as np
import time
import winsound
from itertools import cycle


def _saveimg_(img):
    global nsave
    cv.imwrite('D:/Camaras homeland/savescreen/save'+str(nsave)+'.jpg',img)
    nsave +=1

def sha(img):
    rgb_planes = cv.split(img)
    
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv.medianBlur(dilated_img, 21)
        diff_img = 255 - cv.absdiff(plane, bg_img)
        norm_img = cv.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
    
    result = cv.merge(result_planes)
    result_norm = cv.merge(result_norm_planes)
    
    return result


test = False
video = True
mypc = True

barplayer = []
b = None
thd = 35
morpho = 7
dlt = 1
nframe = 0
detectr = False


if video:
    if mypc:
        cap = cv.VideoCapture('c:/Repositorios/Python/Computer Vision from cameras/videos homeland/Calle Paimun Norte_20220630_082628~20220630_143235.3gp')
    else:
        cap = cv.VideoCapture('')
else:
    cap= cv.VideoCapture('rtsp://homeland:Homeland2019@10.10.1.253:3454/Media/Live/Normal?camera=C_28&streamindex=1')# acceso
    #cap= cv.VideoCapture('rtsp://homeland:Homeland2019@10.10.1.253:3454/Media/Live/Normal?camera=C_3&streamindex=1')


nsave = 0
bar = False

while True:
    if type(cap) == None:
        print('No se recive imagen!!')
        break
    if nframe >= 90000 and test:
        print('FINISH')
        print(str('thd = '+str(thd)))
        print(str('morpho = '+str(morpho)))
        print(str('dlt = '+str(dlt)))
        break
    if test:
        cap = cv.VideoCapture('H:/Repositorios/Python/Camaras homeland/videos homeland/Acceso Principal_20220729_080436~20220729_200550(2).3gp')
    object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=thd,detectShadows=False)
    while(True):
        ret, img = cap.read()
        
        nframe = int(cap.get(cv.CAP_PROP_POS_FRAMES))
        cv.rectangle(img,pt1=(550,35),pt2=(0,0),color=(0,0,0),thickness=-1)
        #cv.putText(img, str(int(cap.get(cv.CAP_PROP_POS_FRAMES))), (0, 25), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        #n += 1
        img = cv.resize(img,(0,0),fx=0.5,fy=0.5)
        #img = sha(img)
        mask = object_detector.apply(img)
        #mask = cv.bilateralFilter(mask, 11, 17, 17)
        #gau_img = cv.GaussianBlur(gray, (5,5), 0)
        #_, threshold_img=cv.threshold(mask, 254, 255, cv.THRESH_BINARY)
        morpho_img = cv.morphologyEx(mask, cv.MORPH_OPEN, cv.getStructuringElement(cv.MORPH_ELLIPSE,(morpho,morpho)))
        dilate_img = cv.dilate(morpho_img,None,iterations=dlt)
        
        (cntr,_)=cv.findContours(dilate_img, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        
        for contour in cntr:
            (x,y,w,h)=cv.boundingRect(contour)
            sup = round(h*w,2)
            asp = round(float(w)/h,2)
            if asp > 0.3 and asp < 1.4 and sup < 10000 and sup > 200:
                if test:
                    detectr = True
                    thd += 1
                    print('frame n°',nframe)
                    break
                else:
                    cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    cv.putText(img,str(sup)+'  '+str(asp), (x, y-5), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    #_saveimg_(img)
                    #print('\a')
                    #frequency = 2500
                    #duration = 1000
                    #winsound.Beep(frequency, duration)
                    #cropp = img[(y-100):(y-100)+(h+100), (x-100):(x-100)+(w+100)]
                    #cropp = img[y:y+h, x:x+w]
                    #cropp = cv.resize(cropp,(0,0),fx=3,fy=3)
                    
                    #cv.imshow('detect',cropp)
                    
                    
                    # reproduccion
                    imgf = img
                    barplayer.append(cv.resize(imgf,(0,0),fx=0.6,fy=0.8))
                    cv.putText(imgf, str(nframe), (0, 25), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    b = cycle(barplayer)
                    bar = True
        if bar:
            frame = next(iter(b)) 
            cv.imshow('bar',frame)
            
            
            
        
        cv.imshow('screen',cv.resize(img,(0,0),fx=1,fy=1))
        #cv.imshow('mask',mask)
        #cv.imshow('dilate',dilate_img)
        #cv.imshow('threshold',dilate_img)
        
        key=cv.waitKey(1)
        if key==ord('q'):
            cap.release()
            cv.destroyAllWindows()
            break
        #if key==ord('r'):
        #    frame = None
        #    cv.destroyWindow('bar')
        #    barplayer = []
        #    b = None
        
        if detectr and test:
            print(' thd = ',thd)
            detectr = False
            break
cap.release()
cv.destroyAllWindows()
        