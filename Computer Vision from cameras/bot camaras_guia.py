import cv2 as cv
import os
from windowcapture import WindowCapture
from vision import Vision
os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('1.3gp - Reproductor multimedia VLC')
target = Vision('H:\Repositorios\Python\Bot eve online/jump.jpg')
while(True):
    screenshot = wincap.get_screenshot()
    points = target.find(1490,60,430,50,screenshot, 0.8, 'rectangles')
    print('X = '+str(points))
    
    
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break