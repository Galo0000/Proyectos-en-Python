import cv2 as cv
import os
from windowcapture import WindowCapture
os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('EVE — Guileo Galo')

while(True):
    if wincap.screenshot is None:
        continue
    screenshot = wincap.get_screenshot()
    cv.imshow('eveonline',screenshot)
    
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        cv.destroyAllWindows()
        break
