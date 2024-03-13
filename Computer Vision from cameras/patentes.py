import cv2 as cv
import os
import imutils
import numpy as np
import correctordevista as cdv
import pytesseract






def sha(img):
    rgb_planes = cv.split(img)
    
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv.dilate(plane, np.ones((5,5), np.uint8))
        bg_img = cv.medianBlur(dilated_img, 21)
        diff_img = 255 - cv.absdiff(plane, bg_img)
        norm_img = cv.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
    
    result = cv.merge(result_planes)
    result_norm = cv.merge(result_norm_planes)
    
    return result_norm

def _saveimg_(img):
    global n
    cv.imwrite('H:/Repositorios/Python/Camara/test/test'+str(n)+'.jpg',img)
    n+=1
    
n = 0
video = True
mypc = True

#constantes
saveimg = False


if video:
    if mypc:
        cap = cv.VideoCapture('H:/Repositorios/Python/Camara/videos/x.3gp')
    else:
        cap = cv.VideoCapture('C:/ProgramData/../x.3gp')
else:
    cap= cv.VideoCapture('rtsp://...')

if mypc == True:
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

wx = 500
yw = 600
wy = 400
xw = 1100

rec = 0
cany = 90


while(True):
    ret, imgo = cap.read()
    try:
        imgo = imgo[wy:wy+yw, wx:wx+xw]
        #imgs = sha(imgo)
    except:
        cap.release()
        cv.destroyAllWindows()
        break
    gray = cv.cvtColor(imgo, cv.COLOR_BGR2GRAY)
    #se = cv.getStructuringElement(cv.MORPH_RECT,(8,8))
    #bg = cv.morphologyEx(imgo , cv.MORPH_DILATE, se)
    #out_gray = cv.divide(imgo,bg,scale=255)
    
    
    #gray = cv.blur(gray, (3,3))
    #bfilter = cv.bilateralFilter(gray, 15, 75, 75)
    edged = cv.Canny(gray, cany, 255)#70,255
    #dilate = cv.dilate(canny, None , iterations=1)
    keypoints = cv.findContours(edged.copy(),cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours,key=cv.contourArea,reverse=True)[:10]
    
    #cv.drawContours(imgo, contours, -1, (0,255,0), 2)
    for i in range(len(contours)):
        x ,y, w, h = cv.boundingRect(contours[i])
        area=w*h    
        aspectRatio = float(w)/h
        a = (w > 80,w < 130,h > 30,h < 80)#,aspectRatio > 1.9,aspectRatio < 3)#,area > 4100,area < 7000)
        if w == 93 and h == 43:
            break
        if w == 113 and h == 47 or h == 48:
            break
        if  all(a):
            approx = cv.approxPolyDP(contours[i], 0.02* cv.arcLength(contours[i], True), True)
            if len(approx) == 4:
                width=w
                height=h   
                start_x=x
                start_y=y
                end_x=start_x+width
                end_y=start_y+height      
                cv.rectangle(imgo, (start_x,start_y), (end_x,end_y), (0,0,255),3)
                cv.putText(imgo,' W: '+str(w)+'  H: '+str(h)+'  AREA: '+str(area)+'  ASP: '+str(aspectRatio), (x, y-5), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                if saveimg:
                    _saveimg_(imgo)
                imgp = gray[(start_y-rec):(start_y-rec)+(height+rec),(start_x-rec):(start_x-rec)+(width+rec)]
                #ret, thresh = cv.threshold(imgp, 150, 255, cv.THRESH_BINARY)
                #imgp = cv.resize(imgo,(0,0),fx=2,fy=2)
                #cv.imshow('patente ori',cv.resize(imgp,(0,0),fx=1,fy=1))
                #try:
                #    filtered_image = cdv.apply_filter(imgp)
                #    threshold_image = cdv.apply_threshold(filtered_image)
                #    cnv, largest_contour = cdv.detect_contour(threshold_image, imgp.shape)
                #    corners,canvas = cdv.detect_corners_from_contour(cnv, largest_contour)
                #    destination_points, h, w = cdv.get_destination_points(corners)
                #    un_warped = cdv.unwarp(threshold_image, np.float32(corners), destination_points)
                #    cropped = un_warped[0:h, 0:w]
                #except:
                #    break
                try:
                    cv.imshow('patente',cv.resize(imgp,(0,0),fx=2,fy=2))
                except:
                    pass
                ocr = pytesseract.image_to_string(imgp).translate({ord(letter): None for letter in '\.¢°|!"#$%&()=?¡¿¨*‘´[]{};,:-_></*-+\'[] '})
                if len(ocr) > 0:
                    ocr = ocr.rstrip(ocr[-1])
                    if not any(c.islower() for c in ocr):
                        print(str(ocr)+' len = '+str(len(ocr)))
    
    #cv.imshow('edged',edged)
    cv.imshow('Video',cv.resize(imgo,(0,0),fx=0.6,fy=0.7))
    #cv.imshow('shadow',imgs)
    #cv.imshow('out_binary',out_binary)
    
  
    if cv.waitKey(1) == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        break