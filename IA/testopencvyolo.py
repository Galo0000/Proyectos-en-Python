
import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while True:
    success, img=cap.read()
    cv2.imshow('image',img)
    cv2.WaitKey(1)