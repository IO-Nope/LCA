import subprocess
import os
import time
import pygetwindow as gw 
import pyautogui as pag
import GameManager
is_debug = 0
bat_file_path = os.path.join(os.path.dirname(__file__),"..","Scripts", "startgame.bat")
gamepath="d:/SteamLibrary/steamapps/common/Limbus Company/LimbusCompany.exe"
# 执行批处理文件并实时输出
process = subprocess.Popen(
    [bat_file_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
    universal_newlines=True
)
while True:
    if(process.stdout is None):
        assert(0)
        break
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
        break
    if output:
        print(output.strip())
stderr = process.communicate()[1]
if stderr or process.returncode!= 0:
    print("Standard Error:")
    print(stderr)
    assert(0)
#检测游戏窗口出现 
def is_window_open(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    return len(windows) > 0
def get_window_position(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        return window.left, window.top, window.width, window.height
    else:
        return None

gametitle = "LimbusCompany"
timeout = 300
while True:
    if is_window_open(gametitle):
        print(f"Game window '{gametitle}'is appeared")
        if(is_debug):
            break
        time.sleep(15)
        break
    else:
        print(f"Game window '{gametitle}'is not appeared waiting...")
        time.sleep(2)
        timeout -= 2
        if timeout <= 0:
            print(f"Game window '{gametitle}'is not appeared in '{timeout}' seconds,timeout!")
            assert(0)
game_pos = get_window_position(gametitle)
if game_pos is None:
    print(f"Game window '{gametitle}'is not found")
    assert(0)
if game_pos is not None:
    left, top, width, height = game_pos
pag.moveTo(left+width / 2, top+height / 2)
subprocess.run([gamepath], shell=True)
if(not is_debug):
    pag.click()

#TODO: 处理一堆东西 比如掉线 更新 等等

#进入游戏

if(not is_debug):
    time.sleep(30)
getGMIns = GameManager.GameWindow.get_instance
getGMIns().init(left, top, width, height)
#getGMIns().move_check()
#getGMIns().switch_box()
getGMIns().daily_clear()
#getGMIns().lux_clear()
#getGMIns().auto_fight()

