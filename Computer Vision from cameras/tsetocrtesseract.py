import cv2
import os
import pytesseract
import matplotlib.pyplot as plt
import time

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

#for file in os.listdir(os.path.join('H:/Repositorios/Python/Camaras homeland/', 'capturas patentes')):
image = cv2.imread('H:/Repositorios/Python/Camaras homeland/capturas patentes/pat114.jpg')#+file)
image = cv2.resize(image,(0,0),fx=2.0,fy=2.0)
for n in range(1,255):
    _, img = cv2.threshold(image, n, 255, cv2.THRESH_BINARY)
    ocr = pytesseract.image_to_string(img)
    #print(ocr,' valor = ',n,' len = ',len(ocr))
    if len(ocr) == 10:# or ocr  == 'AD 885 WM':
        plt.imshow(img)
        plt.title('filtro = '+str(n))
        plt.show()
        print(ocr,' valor = ',n)