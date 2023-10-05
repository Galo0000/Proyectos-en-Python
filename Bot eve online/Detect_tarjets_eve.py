import cv2
import pyautogui
import os
import numpy as np
from windowcapture import WindowCapture
os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('EVE — Guileo Galo')
screenshot = wincap.get_screenshot()
cv2.imshow('Screenshot', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()