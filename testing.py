import pyautogui
import time
import random

try:
    while True:
        pyautogui.press('ctrl')
        print("pressed")
        time.sleep(random.uniform(1.0, 3.0))
except KeyboardInterrupt:
    print("Program stopped by user.")
