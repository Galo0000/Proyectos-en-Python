import cv2 as cv
import os
from windowcapture import WindowCapture
from vision import Vision
import control
import pyautogui
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

targets = []
targets_lock = []
name_target = []
n = 0
# initialize the WindowCapture class
wincap = WindowCapture('EVE - Guileo Galo')
# initialize the Vision class
frigate = Vision('imgeveonline/frigate.jpg')
frigate_lock = Vision('imgeveonline/frigate_lock.jpg')
destroyer = Vision('imgeveonline/destroyer.jpg')
destroyer_lock = Vision('imgeveonline/destroyer_lock.jpg')
cruiser = Vision('imgeveonline/cruiser.jpg')
cruiser_lock =  Vision('imgeveonline/cruiser_lock.jpg')
centry = Vision('imgeveonline/centry.jpg')
centry_lock = Vision('imgeveonline/centry_lock.jpg')


targets.append(frigate)
name_target.append('Frigate')
targets_lock.append(frigate_lock)
targets.append(destroyer)
name_target.append('Destroyer')
targets_lock.append(destroyer_lock)
targets.append(cruiser)
name_target.append('Cruiser')
targets_lock.append(cruiser_lock)
targets.append(centry)
name_target.append('Centry')
targets_lock.append(centry_lock)

engage = False

time.sleep(5)
while(True):
    n = 0
    for (t,tl,name) in zip(targets,targets_lock,name_target):
        while(True):
            pyautogui.moveTo(100, 100)
            time.sleep(1)
            screenshot = wincap.get_screenshot()
            points = t.find(1490,180,31,793,screenshot, 0.8, 'rectangles')
            
            if len(points) > 0:
                
                for p in points[0:5]:
                    winx,winy = wincap.get_screen_position(p)
                    print(str(name)+' = '+str(winx)+'  y = '+str(winy))
                    control.lock_target(winx,winy)
                pyautogui.moveTo(100, 100)
        
                while(True):
                    screenshot = wincap.get_screenshot()
                    points = tl.find(1490,180,31,793,screenshot, 0.8, 'rectangles')
                    
                    if len(points) > 0:
                        print(name+' locked detected')
                        engage = True
                        break
                    
                if engage:
                    while(True):
                        screenshot = wincap.get_screenshot()
                        points = tl.find(1490,180,31,793,screenshot, 0.8, 'rectangles')
                        if len(points) == 0:
                            engage = False
                            break
                        else:
                            pyautogui.press('f')
            else:
                break
    for t in targets:
        time.sleep(4)
        screenshot = wincap.get_screenshot()
        points = t.find(1490,180,31,793,screenshot, 0.8, 'rectangles')
        n += len(points)
    print('n = '+str(n))
    if n == 0:
        print('terminar')
        cv.destroyAllWindows()
        break
    else:
        continue

        
