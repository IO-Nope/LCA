import cv2
import numpy as np
import pyautogui
from PIL import Image
import os
isDebug = 1
def calculate_by_rightdown_centerbase(x, y):
    x = (640-x) / 1280
    y = (360-y) / 1280
    if isDebug:
        print("{:.3f},{:.3f}".format(x,y))
    return x ,y
def calculate_by_rightdown_bottombase(x, y):
    x = (640-x) / 1280
    y = -y / 1280
    if isDebug:
        print("{:.3f},{:.3f}".format(x,y))
    return x ,y
def match_template(screenshot, template):
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template_cv = cv2.cvtColor(np.array(template), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screenshot_cv, template_cv, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if isDebug:
        print("match the max_val is: ", max_val)
    threshold = 0.6 #realated R
    return max_val >= threshold

def load_image_from_path(path):
    images = {}
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img = cv2.imread(file_path)
            if img is not None:
                name, _ = os.path.splitext(filename)
                images[name] = img
    return images