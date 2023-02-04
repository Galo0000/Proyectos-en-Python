import pyautogui
from time import sleep

wait = 0.05

def lock_target(x,y):
    pyautogui.keyDown('ctrl')
    pyautogui.moveTo(x=x,y=y)
    pyautogui.click(button='left')
    pyautogui.keyUp('ctrl')
        
def click(x,y):
    pyautogui.moveTo(x=x,y=y)
    pyautogui.click(clicks=2)
        
def rightclick(x,y):
    pyautogui.click(x=x,y=y,button='right')
    sleep(wait)
        
def align_to(x,y):
    pyautogui.click(x=x,y=y,button='left')
    sleep(wait)
    pyautogui.press('a')
        
def warp_0m(x,y):
    pyautogui.click(x=x,y=y,button='left')
    sleep(wait)
    pyautogui.press('s')
        
def jump(x,y):
    pyautogui.click(x=x,y=y,button='left')
    sleep(wait)
    pyautogui.press('d')
    
def approach(x,y):
    pyautogui.click(x=x,y=y,button='left')
    sleep(wait)
    pyautogui.press('q')
        
def dock(x,y):
    pyautogui.click(x=x,y=y,button='left')
    sleep(wait)
    pyautogui.press('d')
        
def orbit(x,y):
    pyautogui.click(x=x,y=y,button='left')
    sleep(wait)
    pyautogui.press('w')