import cv2 as cv
import os
from windowcapture import WindowCapture
from vision import Vision
import control
import time
import pyautogui
os.chdir(os.path.dirname(os.path.abspath(__file__)))
wincap = WindowCapture('EVE - Guileo Galo')
stargate_travel = Vision('imgeveonline/stargate_travel.jpg')
jump = Vision('imgeveonline/jump.jpg')
nothing_found = Vision('imgeveonline/nothing_found.jpg')
station = Vision('imgeveonline/station.jpg')

time.sleep(3)
while (True):
    pyautogui.moveTo(1000, 200)
    time.sleep(0.5)
    screenshot = wincap.get_screenshot()
    points = stargate_travel.find(1490,180,31,793,screenshot, 0.8, 'rectangles')
    print(points)
    if len(points) > 0:
        print('found!')
        points = points[-1]
        winx,winy = wincap.get_screen_position(points)
        control.click(winx, winy)
        screenshot = wincap.get_screenshot()
        points = jump.find(1490,60,430,50,screenshot, 0.8, 'rectangles')
        if len(points) == 1:
            print(points)
            pyautogui.press('d',presses=2)
            while (True):
                screenshot = wincap.get_screenshot()
                points = nothing_found.find(1490,180,400,200,screenshot, 0.8, 'rectangles')
                if len(points) == 1:
                    time.sleep(1)
                    break
                else:
                    pyautogui.press('d',presses=2)
                    continue