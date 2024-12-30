import time                                 # 引入時間模組，用於延遲操作
import board                                # 引入樹莓派的硬體板模組
import RPi.GPIO as GPIO                     # 引入GPIO控制模組，用於控制引腳
import busio                                # 引入I2C通訊模組
import adafruit_ssd1306                     # 引入Adafruit SSD1306 OLED顯示器驅動程式
from PIL import Image, ImageDraw, ImageFont # 引入圖片處理模組，用於顯示文字
from gpiozero import Button                 # 引入GPIOZero模組，用於處理按鈕
import argparse                             # 引入命令列解析模組

BTN_UP = 17                                 # 定義向上按鈕的GPIO引腳
BTN_DOWN = 27                               # 定義向上按鈕的GPIO引腳
BTN_ENTER = 22                              # 定義確認按鈕的GPIO引腳
BTN_EXIT = 23                               # 定義退出按鈕的GPIO引腳
LED_DMA = 10                                # 定義DMA通道   
button_enter = Button(BTN_ENTER)            # 創建按鈕對象，用於監聽ENTER按鈕
is_running = False                          # 初始化運行標誌，表示程式是否正在運行

ENTER_PIN = BTN_ENTER                       # 定義ENTER按鈕引腳

GPIO.setmode(GPIO.BCM)                                   # 設定GPIO使用BCM編號模式
GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # 設置BTN_UP為輸入並啟用上拉電阻
GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 設置BTN_DOWN為輸入並啟用上拉電阻
GPIO.setup(BTN_ENTER, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 設置BTN_ENTER為輸入並啟用上拉電阻
GPIO.setup(BTN_EXIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 設置BTN_EXIT為輸入並啟用上拉電阻

i2c = busio.I2C(board.SCL, board.SDA)                # 初始化I2C通訊
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c) # 初始化SSD1306 OLED顯示器


image = Image.new('1', (128, 64)) # 創建一個128x64像素的圖像，用來顯示在OLED
draw = ImageDraw.Draw(image)      # 創建一個繪圖對象，用來在圖像上繪製
font = ImageFont.load_default()   # 加載預設字體

led_on = False  # 初始化LED開關狀態
led_mode = None # 初始化LED顯示模式

fun_index = 0   # 初始化功能索引
key_up = True   # 初始化按鈕狀態，按鈕未被按下

# 顯示菜單11
def menu11():
    print("menu11 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) # 清空顯示區域 
    draw.text((0, 0), "     ", fill=255)               # 顯示標題(無)
    draw.text((0, 20), "-> 1", fill=255)             # 顯示菜單選項
    draw.text((0, 40), "   2", fill=255)  # 顯示菜單選項
    display.image(image)                               # 將圖像顯示到OLED
    display.show()

def menu12():
    print("menu12 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) 
    draw.text((0, 0), "     ", fill=255)              
    draw.text((0, 20), "   1", fill=255)             
    draw.text((0, 40), "-> 2", fill=255)  
    display.image(image)                               
    display.show()  

def menu21():
    global led_on, led_mode                           
    print("menu21 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)      
    draw.text((0, 20), "   3", fill=255)            
    display.image(image)                            
    display.show()


def menu24():
    print("menu24 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) 
    draw.text((0, 20), "   4", fill=255)   
    display.image(image) 
    display.show()  

def key_scan():
    global key_up                                      # 聲明全局變量 key_up，用於控制按鍵是否已鬆開，防止重複觸發
    # 檢查 key_up 狀態，確保只有在按鍵完全鬆開後才處理新的按鍵按下事件
    if key_up:                                         # 檢查 key_up 狀態，確保只有在按鍵完全鬆開後才處理新的按鍵按下事件
        # 檢查按鍵 BTN_UP 是否被按下
        if GPIO.input(BTN_UP) == GPIO.LOW:             # 檢查按鍵 BTN_UP 是否被按下
            key_up = False                             # 標記按鍵進入按下狀態，避免重複觸發
            print("Button UP pressed")                 # 輸出按下 BTN_UP 的提示
            return 4                                   # 返回代碼 4 表示 "向上" 按鈕被按下
        # 檢查按鍵 BTN_DOWN 是否被按下
        elif GPIO.input(BTN_DOWN) == GPIO.LOW:         # 檢查按鍵 BTN_DOWN 是否被按下
            key_up = False                             # 標記按鍵進入按下狀態
            print("Button DOWN pressed")               # 輸出按下 BTN_DOWN 的提示
            return 3                                   # 返回代碼 3 表示 "向下" 按鈕被按下
        # 檢查按鍵 BTN_ENTER 是否被按下
        elif GPIO.input(BTN_ENTER) == GPIO.LOW:        # 檢查按鍵 BTN_ENTER 是否被按下
            key_up = False                             # 標記按鍵進入按下狀態
            print("Button ENTER pressed")              # 輸出按下 BTN_ENTER 的提示
            return 1                                   # 返回代碼 1 表示 "確定" 按鈕被按下
        # 檢查按鍵 BTN_EXIT 是否被按下
        elif GPIO.input(BTN_EXIT) == GPIO.LOW:         # 檢查按鍵 BTN_EXIT 是否被按下
            key_up = False                             # 標記按鍵進入按下狀態
            print("Button EXIT pressed")               # 輸出按下 BTN_EXIT 的提示
            return 2                                   # 返回代碼 2 表示 "退出" 按鈕被按下
        # 如果所有按鍵均未被按下（所有按鈕均處於高電位狀態） 
    if (GPIO.input(BTN_UP) == GPIO.HIGH and            # BTN_UP 未被按下       
        GPIO.input(BTN_DOWN) == GPIO.HIGH and          # BTN_DOWN 未被按下
        GPIO.input(BTN_ENTER) == GPIO.HIGH and         # BTN_ENTER 未被按下
        GPIO.input(BTN_EXIT) == GPIO.HIGH):            # BTN_EXIT 未被按下
        key_up = True                                  # 將 key_up 標記為 True，表明按鍵已完全鬆開
        print("All buttons released")                  # 輸出所有按鈕鬆開的提示
    return 0    

key_table = [                                          #menuXX上下左右對應的菜單
    {'up': 0, 'down': 1, 'enter': 2, 'exit': 0, 'operation': menu11},
    {'up': 0, 'down': 1, 'enter': 3, 'exit': 0, 'operation': menu12},
    {'up': 2, 'down': 2, 'enter': 2, 'exit': 0, 'operation': menu21},
    {'up': 2, 'down': 3, 'enter': 3, 'exit': 1, 'operation': menu24},
]

def run_menu():
    global fun_index                                   # 追蹤當前的功能索引，指向當前菜單
    key_input = key_scan()                             # 獲取用戶輸入的按鍵（如：UP、DOWN、ENTER、EXIT）
    print(f"Current fun_index: {fun_index}")           # 顯示當前菜單的索引，幫助調試
    # 根據按下的按鍵執行不同的操作
    if key_input == 4:                                 # UP (當 UP 鍵被按下)
        print(f"Going UP to {key_table[fun_index]['up']}") # 顯示將轉向的上級菜單
        fun_index = key_table[fun_index]['up']         # 根據目前菜單的 'up' 欄位設定菜單索引
        key_table[fun_index]['operation']()            # 執行對應菜單的操作函數
    elif key_input == 3:                               # DOWN (當 DOWN 鍵被按下)
        print(f"Going DOWN to {key_table[fun_index]['down']}") # 顯示將轉向的下級菜單
        fun_index = key_table[fun_index]['down']       # 根據目前菜單的 'down' 欄位設定菜單索引
        key_table[fun_index]['operation']()            # 執行對應菜單的操作函數
    elif key_input == 1:                               # ENTER (當 ENTER 鍵被按下)
        print(f"ENTER pressed at menu {fun_index}")    # 顯示當前菜單索引
        fun_index = key_table[fun_index]['enter']      # 根據目前菜單的 'enter' 欄位設定菜單索引
        key_table[fun_index]['operation']()            # 執行對應菜單的操作函數
    elif key_input == 2:                               # EXIT (當 EXIT 鍵被按下)
        print(f"EXIT pressed at menu {fun_index}")     # 顯示當前菜單索引
        fun_index = key_table[fun_index]['exit']       # 根據目前菜單的 'exit' 欄位設定菜單索引
        key_table[fun_index]['operation']()            # 執行對應菜單的操作函數

    
menu11()                                               # 顯示菜單 11，這會初始化第一個菜單並顯示它

try:                                                   
    while True:                                        # 使用無窮迴圈來不斷運行菜單系統，直到用戶中斷
        run_menu()                                     # 調用 run_menu 函數處理按鍵輸入並執行對應的菜單操作
        time.sleep(0.01)                               # 短暫延遲，防止 CPU 過度運行，並減少高頻次輪詢按鍵的負擔
except KeyboardInterrupt:                              # 捕獲使用者手動中斷（Ctrl+C），並顯示結束訊息
    print("Program terminated")
finally:
    GPIO.cleanup()                                     # 無論程式是否正常終止，都會執行 GPIO.cleanup() 清理 GPIO 引腳的狀態，防止硬體狀態不一致