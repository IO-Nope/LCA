import subprocess
import os
import time
import pygetwindow as gw 
import pyautogui as pag
import GameManager
is_debug = 1
getGMins = GameManager.GameManager.get_instance

getGMins().start_game()
