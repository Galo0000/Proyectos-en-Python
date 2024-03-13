import torch
import cv2
import numpy as np
import os
import pytesseract
import string
import matplotlib.pyplot as plt
import time
import correctordevista as cv
import threading as th

def task():
    global ret,img
    while True:
        ret, img = cap.read()

def _saveimg_(img):
    global n
    cv2.imwrite('D:/Camara/pat'+str(n)+'.jpg',img)
    n+=1


def sha(img):
    rgb_planes = cv2.split(img)
    
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
    
    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    
    return result_norm

frame_rate = 1
prev = 0
times = 0
#n = 1
imglist = []
video = False
mypc = False
img = None
ret = None

#os.chdir(os.path.dirname(os.path.abspath(__file__)))

if video:
    if mypc:
        cap = cv2.VideoCapture('H:/Repositorios/Python/Camara/videos/x.3gp')
    else:
        cap = cv2.VideoCapture('C:/ProgramData/../x.3gp')
else:
    cap= cv2.VideoCapture('rtsp://..')
    cap.set(cv2.CAP_PROP_BUFFERSIZE,1)

    
if mypc == True:
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    model = torch.hub.load('ultralytics/yolov5','custom', path = 'H:/Repositorios/Python/Camara/bests.pt')
else:
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    model = torch.hub.load('ultralytics/yolov5','custom', path = 'D:/Camara/bests.pt')

model.conf = 0.85
#t = th(task)
#t.start()

while 1:
    time_elapsed = time.time() - prev
    ret, img = cap.read()
    if not ret:
        break
    if time_elapsed > 1./frame_rate:
        prev = time.time()
        try:
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = img[400:400+600, 500:500+1100]# live
            #img = img[289:289+500, 228:228+800]
            #img = img[500:500+400, 400:400+1100]# video test
        except:
            cap.release()
            cv2.destroyAllWindows()
            break
        #img = cv2.resize(img,(0,0),fx=0.9,fy=1.0)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detect = model(img)
        info = detect.pandas().xyxy[0]
        if len(info) > 0:
            #print(info.iloc[0]['confidence'])
            xmin = int(info.iloc[-1]['xmin'])
            xmax = int(info.iloc[-1]['xmax'])
            ymin = int(info.iloc[-1]['ymin'])
            ymax = int(info.iloc[-1]['ymax'])
            m = (ymin > 0, ymax > 0,xmin > 0 ,xmax > 0)
            if not all(m):
                continue
            #mask = np.zeros(gray.shape,np.uint8)
            #location = np.array([[ymax,xmin],[ymax,xmax],[ymin,xmax],[ymin,xmin]],dtype = np.int)
            img = img[ymin:ymin+(ymax-ymin),xmin:xmin+(xmax-xmin)]
            
            img = cv2.resize(img,(0,0),fx=1.9,fy=2.0)
            #img = sha(img)
            #new_image = cv2.drawContours(mask,location,0,255,-1)
            #new_image = cv2.bitwise_and(img,img,mask=mask)
            #_, img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
            #img = cv2.dilate(img,None,iterations=1)
            
            
            #imglist.append(img)
            #if times == 0:
            #    times = 0
            #else:
            #    times += 1
            #    continue
            #for e,i in enumerate(imglist):
    
            filtered_image = cv.apply_filter(img)
            threshold_image = cv.apply_threshold(filtered_image)
            cnv, largest_contour = cv.detect_contour(threshold_image, img.shape)
            corners,canvas = cv.detect_corners_from_contour(cnv, largest_contour)
            #cv2.imshow('canvas',canvas)
            destination_points, h, w = cv.get_destination_points(corners)
            un_warped = cv.unwarp(threshold_image, np.float32(corners), destination_points)
    
                    
            cropped = un_warped[0:h, 0:w]
                
                #f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
                #ax1.imshow(un_warped)
                #ax2.imshow(cropped)
                
                #plt.show()
                #_, thg = cv2.threshold(cropped, 140, 255, cv2.THRESH_BINARY)
                
                #plt.imshow(cropped)
                #plt.title('patente '+str(e))
                #plt.show()
                
            cv2.imshow('patente ',cropped)#+str(e),cropped)
                
                #plt.imshow(crop_img)
                #plt.title(info.iloc[0]['confidence'])
                #plt.show()
                ##
            ocr = pytesseract.image_to_string(threshold_image).translate({ord(letter): None for letter in '\.¢°|!"#$%&()=?¡¿¨*‘´[]{};,:-_></*-+\'[] '})
            if len(ocr) > 0:
                ocr = ocr.rstrip(ocr[-1])
                if not any(c.islower() for c in ocr):
                    print(str(ocr)+' len = '+str(len(ocr))+' '+str(info.iloc[0]['confidence']))
            #imglist = []
            

    
    cv2.imshow('detector patentes',cv2.resize(np.squeeze(detect.render()),(0,0),fx=0.4,fy=.5))
    
    
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()