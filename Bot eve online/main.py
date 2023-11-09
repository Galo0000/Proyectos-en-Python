import cv2 as cv
import os
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from edgefilter import EdgeFilter


os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
wincap = WindowCapture('EVE - Guileo Galo')
# initialize the Vision class
#vision_jump = Vision('imgeveonline/jump.jpg')
#vision_jump.init_control_gui()


while(True):
    
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    
    #processed_image = vision_jump.apply_hsv_filter(screenshot)
    #edges_image = vision_jump.apply_edge_filter(processed_image)
    
    #cv.imshow('Processed', processed_image)
    #cv.imshow('Edges', edges_image)
    cv.imshow('eveonline', screenshot)
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
