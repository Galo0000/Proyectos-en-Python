import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import correctordevista as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


for file in os.listdir(os.path.join('H:/Repositorios/Python/Camara/', 'capturas patentes')):
    imageh = cv2.imread('H:/Repositorios/Python/Camara/capturas patentes/'+file)
    image = cv2.resize(imageh,(0,0),fx=5.0,fy=5.0)
    
    plt.imshow(image)
    plt.title('Original Image')
    plt.show()
    
    filtered_image = cv.apply_filter(image)
    threshold_image = cv.apply_threshold(filtered_image)
    
    
    try:
        cnv, largest_contour = cv.detect_contour(threshold_image, image.shape)
        corners = cv.detect_corners_from_contour(cnv, largest_contour)
    except:
        pass
    
    destination_points, h, w = cv.get_destination_points(corners)
    un_warped = cv.unwarp(image, np.float32(corners), destination_points)
    
    cropped = un_warped[0:h, 0:w]
    #f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    #ax1.imshow(un_warped)
    #ax2.imshow(cropped)
    
    #plt.show()
    _, thg = cv2.threshold(cropped, 140, 255, cv2.THRESH_BINARY)
    ocr = pytesseract.image_to_string(thg)
    plt.imshow(thg)
    plt.title(str(ocr))
    plt.show()