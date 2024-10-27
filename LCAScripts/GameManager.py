
import pygetwindow as gw 
import pyautogui as pag
import Vector2
import time
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
from Utils.utils import *
import random
from PIL import Image
import subprocess


is_debug = False
sleeptime = 1.5
class GameWindow:
    __instance = None
    #region properties
    __buttons = {}
    __imgines = {}
    __behaiors_senddata = []
    __lefttop = Vector2.Vector2(0,0)
    __size = Vector2.Vector2(0,0)
    __center = Vector2.Vector2(0,0)
    __panelcenter = Vector2.Vector2(0,0)
    
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls(0,0,0,0)
        return cls.__instance
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    def __init__(self, left, top, width, height):
        if not self.__instance:
            self.__lefttop = Vector2.Vector2(left, top)
            self.__size = Vector2.Vector2(width, height)
            self.__instance = self
    def __check(self):
        if self.__size.x < 1280 or self.__size.y < 720:
            return False
        return True
    def __locate_center(self , x,y):
        return self.__center.x + x*self.__size.x, self.__center.y + y*self.__size.x
    def __locate_bottomCenter(self, x,y):
        return self.__center.x + x*self.__size.x, self.__lefttop.y + self.__size.y + y*self.__size.x
    def __locate_topRight(self, x,y):
        return self.__lefttop.x + self.__size.x + x*self.__size.x, self.__lefttop.y +40 + y*self.__size.x
    def __init(self):
        #region init buttons
        self.__center = self.__lefttop + self.__size/2
        self.__center.y = self.__center.y + 20 #The margin of the top
        self.__buttons["center"]=self.__center
        
        tempx = self.__center.x
        tempy = self.__lefttop.y + self.__size.y
        tempy = tempy - 0.09*self.__size.x/2
        self.__panelcenter = Vector2.Vector2(tempx, tempy)
        self.__buttons["panelcenter"] = self.__panelcenter
        
        self.__buttons["entergame"] = Vector2.Vector2(self.__center.x, self.__center.y)
        
        tempx = self.__center.x + 0.09375*self.__size.x
        tempy = self.__center.y + 0.136*self.__size.x
        self.__buttons["bar_confirm"] = Vector2.Vector2(tempx, tempy)
        
        tempx = self.__center.x - 0.09375*self.__size.x
        tempy = self.__center.y + 0.136*self.__size.x
        self.__buttons["bar_cancel"] = Vector2.Vector2(tempx, tempy)
        
        tempx = self.__center.x + 0.1875*self.__size.x
        self.__buttons["drive"] = Vector2.Vector2(tempx, self.__panelcenter.y)
        
        tempx = self.__center.x - 0.144*self.__size.x
        tempy = self.__center.y - 0.156*self.__size.x
        self.__buttons["lux"] = Vector2.Vector2(tempx, tempy)
        
        tempx = self.__center.x + 0.367*self.__size.x
        tempy = self.__center.y + 0.089*self.__size.x
        self.__buttons["lux_max"] = Vector2.Vector2(tempx, tempy)
        
        tempx = self.__center.x + 0.394*self.__size.x
        tempy = self.__center.y + 0.175*self.__size.x
        self.__buttons["startbattle"] = Vector2.Vector2(tempx, tempy)
        
        tempx = self.__center.x - 0.382*self.__size.x
        tempy = self.__center.y - 0.023*self.__size.x
        self.__buttons["bond"] = Vector2.Vector2(tempx, tempy)

        tempx , tempy = self.__locate_center(-0.203,0.090)
        self.__buttons["bondentry"] = Vector2.Vector2(tempx, tempy)
        
        tempx , tempy = self.__locate_center(0,0.094)
        self.__buttons["bond_max"] = Vector2.Vector2(tempx, tempy)
        
        tempx , tempy = self.__locate_center(0.023,0.219)
        self.__buttons["window"] = Vector2.Vector2(tempx, tempy)
        
        tempx , tempy = self.__locate_center(0.355,-0.109)
        self.__buttons["passport"] = Vector2.Vector2(tempx, tempy)
        
        tempx , tempy = self.__locate_center(-0.211,-0.234)
        self.__buttons["passporttask"] = Vector2.Vector2(tempx, tempy)

        tempx , tempy = self.__locate_center(-0.109,-0.109)
        self.__buttons["dailytask"] = Vector2.Vector2(tempx, tempy)
        
        x,y =   calculate_by_rightdown_centerbase(275,220)
        tempx, tempy = self.__locate_center(x,y)
        self.__buttons["confirmLU"] = Vector2.Vector2(tempx, tempy)
        
        x,y =   calculate_by_rightdown_centerbase(70,118)
        tempx, tempy = self.__locate_center(x,y)
        self.__buttons["confirmRD"] = Vector2.Vector2(tempx, tempy)
        
        x = -0.190
        y = 0.0078
        tempx, tempy = self.__locate_topRight(x,y)
        self.__buttons["fightproceesLU"] = Vector2.Vector2(tempx, tempy)
        
        x = -0.148 
        y = 0.0468 
        tempx, tempy = self.__locate_topRight(x,y)
        self.__buttons["fightproceesRD"] = Vector2.Vector2(tempx, tempy)
        
        if(not self.__check()):
            raise Exception("Game window is too small or not found!")
        #endregion init buttons
        #region init images
        self.__imgines = load_image_from_path(os.path.join(os.path.dirname(__file__),"..","Image"))
        #endregion init images
    def init(self, left, top, width, height):
        self.__lefttop = Vector2.Vector2(left, top)
        self.__size = Vector2.Vector2(width, height)
        self.__init()
    def init_vector2(self, lefttop, size):
        self.__lefttop = lefttop
        self.__size = size
        self.__init()
    def init_auto(self):
        self.__init()
    def move_check(self):
        for name, button in self.__buttons.items():
            pag.moveTo(button.x, button.y)
            
            print(f"Move to button {name} : {button}")
            time.sleep(3)
    def move_to(self, buttonname):
        if(buttonname not in self.__buttons):
            print(f"Button {buttonname} not found!")
            return
        pag.moveTo(self.__buttons[buttonname].x, self.__buttons[buttonname].y)
    #TODO: check and deal with lose connection
    def is_lose_connection(self):
        return False
    def deal_lose_connection(self):
        return True
    def click(self, buttonname):
        if(buttonname not in self.__buttons):
            print(f"Button {buttonname} not found!")
            return
        pag.moveTo(self.__buttons[buttonname].x, self.__buttons[buttonname].y)
        while(self.is_lose_connection()):
            self.deal_lose_connection()
            pag.moveTo(self.__buttons[buttonname].x+random.randint(-5, 5), self.__buttons[buttonname].y+random.randint(-5, 5))
        time.sleep(sleeptime)
        
        pag.click()
    def switch_box(self):
        energebarx = self.__lefttop.x + 0.3 * self.__size.x
        pag.moveTo(energebarx, self.__panelcenter.y)
        time.sleep(1)
        pag.click()
        #切换到狂气
        tempy = self.__center.y - 0.105 * self.__size.x
        pag.moveTo(self.__center.x, tempy)
        time.sleep(1)
        pag.click()
        #确认键
        tempx = self.__center.x + 0.09375*self.__size.x
        tempy = self.__center.y + 0.136*self.__size.x
        pag.moveTo(tempx, tempy)
        time.sleep(2*sleeptime)
        pag.click()
        time.sleep(2*sleeptime)
        pag.click()
        #切换到模块
        tempy = self.__center.y - 0.105 * self.__size.x
        tempx = self.__center.x - 0.105*self.__size.x
        pag.moveTo(tempx, tempy)
        time.sleep(1)
        pag.click()
        
        #模块最大值
        tempx = self.__center.x + 0.125*self.__size.x
        tempy = self.__center.y - 0.025*self.__size.x
        pag.moveTo(tempx, tempy)
        time.sleep(1)
        pag.click()
        self.click("bar_confirm")
        self.click("bar_cancel")
        #TODO: 是否成功
    def p_enter(self):
        pag.click(self.__buttons["entergame"].x, self.__buttons["entergame"].y)
        time.sleep(0.3*sleeptime)
        pag.press("p")
        time.sleep(0.6*sleeptime)
        pag.press("enter")
    
    def get_region(self, VectorLU, VectorRD):
        aimLU = self.__buttons[VectorLU]
        #pag.moveTo(aimLU.x, aimLU.y)
        #time.sleep(sleeptime)
        aimRD = self.__buttons[VectorRD]
        #time.sleep(sleeptime)
        #pag.moveTo(aimRD.x, aimRD.y)
        if aimLU.x > aimRD.x or aimLU.y > aimRD.y:
            raise Exception("LU must be left-top and RD must be right-down")
        if aimLU is None or aimRD is None:
            raise Exception("Vector not found")
        if aimLU.x < 0 or aimLU.y < 0:
            print(f"Region: {aimLU.x}, {aimLU.y}, {aimRD.x - aimLU.x}, {aimRD.y - aimLU.y}")
            raise Exception("Vector out of screen")
        print(f"Region: {aimLU.x}, {aimLU.y}, {aimRD.x - aimLU.x}, {aimRD.y - aimLU.y}")
        return(aimLU.x, aimLU.y, aimRD.x - aimLU.x, aimRD.y - aimLU.y)
    def events_deal(self):
        #TODO: 处理事件
        return
    def auto_fight(self):
        while True:
            #与战斗开始process模糊匹配 成功则退出等待状态
            shotregion = self.get_region("fightproceesLU", "fightproceesRD")
            screenshot = pyautogui.screenshot(region=shotregion)
            if match_template(screenshot, self.__imgines["fightprocess"]):
                break
            shotregion = self.get_region("confirmLU", "confirmRD")
            screenshot = pyautogui.screenshot(region=shotregion)
            if match_template(screenshot, self.__imgines["confirm_cn"]) or match_template(screenshot, self.__imgines["confirm_en"]):
                print("dectect battle end")
                break
            time.sleep(3*sleeptime)
            print("waiting for battle entering...")
        while True:
            #TODO: 战斗中出现的选项匹配
            #与战斗process模糊匹配 成功则退出等待状态
            shotregion = self.get_region("fightproceesLU", "fightproceesRD")
            screenshot = pyautogui.screenshot(region=shotregion)
            if match_template(screenshot, self.__imgines["fightprocess"]):
                print("auto fighting...")
                self.p_enter()
                continue
            #与战斗结束奖励部分模糊匹配 成功则退出采光
            shotregion = self.get_region("confirmLU", "confirmRD")
            screenshot = pyautogui.screenshot(region=shotregion)
            if match_template(screenshot, self.__imgines["confirm_cn"]) or match_template(screenshot, self.__imgines["confirm_en"]):
                print("dectect battle end")
                time.sleep(sleeptime)
                #与采光结束确认匹配 若不匹配则enter
                shotregion = self.get_region("confirmLU", "confirmRD")
                screenshot = pyautogui.screenshot(region=shotregion)
                while match_template(screenshot, self.__imgines["confirm_cn"]) or match_template(screenshot, self.__imgines["confirm_en"]):
                    pag.press("enter")
                    shotregion = self.get_region("confirmLU", "confirmRD")
                    screenshot = pyautogui.screenshot(region=shotregion)
                    time.sleep(0.7*sleeptime)
                return
            time.sleep(2*sleeptime)
            print("waiting for round ending...")
        return
    def lux_clear(self):
        self.click("drive")
        self.click("lux")
        self.click("lux_max")
        self.click("startbattle")
        time.sleep(3*sleeptime)
        self.auto_fight()
        pag.press("esc")
        self.click("window")    
    def bond_clear(self):
        self.click("drive")
        self.click("bond")
        self.click("bondentry")
        self.click("bond_max")
        self.click("startbattle")
        time.sleep(3*sleeptime)
        self.auto_fight()
        pag.press("esc")
        self.click("window")
    def daily_clear(self):
        self.click("drive")
        self.click("lux")
        self.click("lux_max")
        self.click("startbattle")
        time.sleep(3*sleeptime)
        self.auto_fight()
        self.click("bond")
        for i in range(3):
            self.click("bondentry")
            self.click("bond_max")
            self.click("startbattle")
            time.sleep(3*sleeptime)
            self.auto_fight()
        time.sleep(sleeptime)
        pag.press("esc")
        self.click("window")
        self.click("passport")
        self.click("passporttask")
        for i in range(5):
            tempy = self.__buttons["dailytask"].y + 0.070*i*self.__size.x
            pag.moveTo(self.__buttons["dailytask"].x, tempy)
            time.sleep(sleeptime)
            pag.click()
        #deal with some solutions
        time.sleep(sleeptime)
        pag.press("esc")
        #TODO: 是否成功
    def start_game(self):
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
                #TODO:
                time.sleep(15)
                break
            else:
                print(f"Game window '{gametitle}'is not appeared waiting...")
                time.sleep(2)
                timeout-= 2
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
