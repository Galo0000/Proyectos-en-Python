import cv2 as cv
from windowcapture import WindowCapture
from vision import Vision
import control
import os
import pyautogui
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

targets = []
targets_lock = []
name_target = []

wincap = WindowCapture('EVE — Guileo Galo')


centry = Vision('imgeveonline/centry.jpg')
centry_lock = Vision('imgeveonline/centry_lock.jpg')
nothing_found = Vision('imgeveonline/nothing_found.jpg')
frigate = Vision('imgeveonline/frigate.jpg')
frigate_lock = Vision('imgeveonline/frigate_lockv2.jpg')
destroyer = Vision('imgeveonline/destroyer.jpg')
destroyer_lock = Vision('imgeveonline/destroyer_lock.jpg')
cruiser = Vision('imgeveonline/cruiser.jpg')
cruiser_lock =  Vision('imgeveonline/cruiser_lock.jpg')




targets.append(centry)
name_target.append('Centry')
targets_lock.append(centry_lock)
targets.append(frigate)
name_target.append('Frigate')
targets_lock.append(frigate_lock)
targets.append(destroyer)
name_target.append('Destroyer')
targets_lock.append(destroyer_lock)
targets.append(cruiser)
name_target.append('Cruiser')
targets_lock.append(cruiser_lock)


time.sleep(3)
print('Liberando drones..')
pyautogui.keyDown('shift')
pyautogui.press('f')
pyautogui.press('f')
pyautogui.keyUp('shift')
while(True):
    list_targets = []
    pyautogui.moveTo(1000, 200)
    time.sleep(0.3)
    screenshot = wincap.get_screenshot()
    cv.rectangle(screenshot, (1490,31), ((1490+180),(31+793)), (0, 255, 0), 2)
    cv.imshow('eveonline',screenshot)
    for (t,name) in zip(targets,name_target):
        print('Buscando objetivos tipo : '+name)
        points = t.find(1490,180,31,793,screenshot, 0.8, 'rectangles')
        for p in points:
            list_targets.append(p)
    
    
    
    if len(list_targets) > 0:
        print('Objetivos encontrados')
        for tar in list_targets[0:5]:
            winx,winy = wincap.get_screen_position(tar)
            print('Objetivo = '+str(winx)+'  y = '+str(winy))
            control.lock_target(winx,winy)
        
        while(True):
            pyautogui.moveTo(1000, 200)
            for tl in targets_lock:
                time.sleep(0.3)
                screenshot = wincap.get_screenshot()
                print('Buscando naves locked')
                points = tl.find(1490,180,31,793,screenshot, 0.75, 'rectangles')
            
            if len(points) > 0:
                pyautogui.press('f')
            
            else:
                break
    else:            
        screenshot = wincap.get_screenshot()
        print('Buscando naves..')
        points = nothing_found.find(1490,180,400,200,screenshot, 0.8, 'rectangles')
        if len(points) == 1:
            print('terminar')
            print('Guardando drones..')
            pyautogui.keyDown('shift')
            pyautogui.press('r')
            pyautogui.press('r')
            pyautogui.keyUp('shift')
            cv.destroyAllWindows()
            break
        else:
            continue