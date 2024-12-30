import time
import board
import RPi.GPIO as GPIO
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from rpi_ws281x import PixelStrip, Color
from gpiozero import Button
import argparse

BTN_UP = 17
BTN_DOWN = 27
BTN_ENTER = 22
BTN_EXIT = 23
LED_COUNT = 16        
LED_PIN = 18          
LED_FREQ_HZ = 800000  
LED_DMA = 10          
LED_BRIGHTNESS = 255  
LED_INVERT = False    
LED_CHANNEL = 0    
button_enter = Button(BTN_ENTER) 
is_running = False

ENTER_PIN = BTN_ENTER

GPIO.setmode(GPIO.BCM)  
GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(BTN_ENTER, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(BTN_EXIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


image = Image.new('1', (128, 64)) 
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

led_on = False
led_mode = None 

fun_index = 0
key_up = True

segments = {
    'a': 25,   # GPIO 25
    'b': 5,    # GPIO 5
    'c': 6,    # GPIO 6
    'd': 12,   # GPIO 12
    'e': 13,   # GPIO 13
    'f': 14,   # GPIO 14
    'g': 15,   # GPIO 15
    'x': 16,   # GPIO 16
    'dp': 19,  # GPIO 19 
    '1': 20,   # GPIO 20
    '2': 21,   # GPIO 21
    '3': 26    # GPIO 26
}

for segment in segments.values():
    GPIO.setup(segment, GPIO.OUT, initial=GPIO.LOW)

digit_map = {
    '0': ['a', 'b', 'c', 'd', 'e', 'f'],      # 0
    '1': ['b', 'c'],                          # 1
    '2': ['a', 'b', 'd', 'e', 'g'],           # 2
    '3': ['a', 'b', 'c', 'd', 'g'],           # 3
    '4': ['b', 'c', 'f', 'g'],                # 4
    '5': ['a', 'c', 'd', 'f', 'g'],           # 5
    '6': ['a', 'c', 'd', 'e', 'f', 'g'],       # 6
    '7': ['a', 'b', 'c'],                     # 7
    '8': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],  # 8
    '9': ['a', 'b', 'c', 'd', 'f', 'g'],       # 9
    'A': ['a'],# A
    'B': ['b'],# B
    'C': ['c'],# C
    'D': ['d'],# D
    'E': ['e'],# E
    'F': ['f'],# F
    'G': ['g'],# G
    'dp':['dp'],
    'OFF': [0, 0, 0, 0, 0, 0, 0, 0]
}

for pin in segments.values():
    GPIO.setup(pin, GPIO.OUT)

def display_digit(digit):
    for pin in segments.values():
        GPIO.output(pin, GPIO.LOW)
    

    segments_state = digit_map[digit]
    for segment in segments_state:
        GPIO.output(segments[segment], GPIO.HIGH)


def menu11():
    print("menu11 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)  
    draw.text((0, 0), "     ", fill=255)  
    draw.text((0, 20), "-> RGB", fill=255) 
    draw.text((0, 40), "   Seven sections", fill=255) 
    display.image(image)
    display.show()

def menu12():
    print("menu12 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) 
    draw.text((0, 0), "      ", fill=255)  
    draw.text((0, 20), "   RGB", fill=255)  
    draw.text((0, 40), "-> Seven sections", fill=255) 
    display.image(image) 
    display.show()  

def menu21():
    global led_on, led_mode
    print("menu21 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((0, 0), "-> All light", fill=255)
    draw.text((0, 20), "   running water", fill=255)
    draw.text((0, 40), "   RGB", fill=255)
    display.image(image)
    display.show()

    if button_enter.is_pressed:
        while button_enter.is_pressed:
            time.sleep(0.1)
        if led_mode != 'white':
            led_mode = 'white'
            led_on = True
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(255, 255, 255))
            strip.show()
            while True:
                if button_enter.is_pressed:
                    while button_enter.is_pressed:
                        time.sleep(0.1)               
                    led_mode = None
                    led_on = False
                    for i in range(strip.numPixels()):
                        strip.setPixelColor(i, Color(0, 0, 0))
                    strip.show()
                    break


def menu22():
    global led_on, led_mode 
    print("menu22 is being displayed") 
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) 
    draw.text((0, 0),  "   All light", fill=255)  
    draw.text((0, 20), "-> running water", fill=255) 
    draw.text((0, 40), "   RGB", fill=255)  
    display.image(image) 
    display.show()  

    if button_enter.is_pressed:  
        while button_enter.is_pressed:
            time.sleep(0.1)
        if led_mode != 'water':  
            led_mode = 'water' 
            led_on = True  
            while led_mode == 'water': 
                for i in range(strip.numPixels()): 
                    strip.setPixelColor(i, Color(0, 0, 255))  
                    strip.show()  
                    time.sleep(0.1)  
                    strip.setPixelColor(i, Color(0, 0, 0))
                if button_enter.is_pressed:
                    while button_enter.is_pressed:                         
                        time.sleep(0.1)
                    led_mode = None
                    led_on = False
                    for i in range(strip.numPixels()):
                        strip.setPixelColor(i, Color(0, 0, 0)) 
                    strip.show()
                    break
    else:  
        led_mode = None  
        led_on = False 
        for i in range(strip.numPixels()):  
            strip.setPixelColor(i, Color(0, 0, 0))  
        strip.show()  


def menu23():
    global led_on, led_mode
    print("menu23 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((0, 0), "   All light", fill=255)
    draw.text((0, 20), "   running water", fill=255)
    draw.text((0, 40), "-> RGB ", fill=255)
    display.image(image)
    display.show()

    if button_enter.is_pressed:
        while button_enter.is_pressed:  
            time.sleep(0.1)

        if led_mode != 'RGB Gradient':
            led_mode = 'RGB Gradient'
            led_on = True

            red = 255
            green = 0
            blue = 0

            while led_mode == 'RGB Gradient':
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(red, green, blue))
                strip.show()
                if red > 0 and blue == 0: 
                    red -= 5
                    green += 5
                elif green > 0 and red == 0: 
                    green -= 5
                    blue += 5
                elif blue > 0 and green == 0: 
                    blue -= 5
                    red += 5

                red = max(0, min(255, red))
                green = max(0, min(255, green))
                blue = max(0, min(255, blue))

                time.sleep(0.05) 

                if button_enter.is_pressed:
                    while button_enter.is_pressed:  
                        time.sleep(0.1)
                    led_mode = None
                    led_on = False
                    for i in range(strip.numPixels()):
                        strip.setPixelColor(i, Color(0, 0, 0)) 
                    strip.show()
                    break
    else:
        led_mode = None
        led_on = False
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))  
        strip.show()

def menu24():
    print("menu24 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) 
    draw.text((0, 0), " ", fill=255)  
    draw.text((0, 20), "-> 0~9", fill=255)  
    draw.text((0, 40), "   A~G", fill=255) 
    display.image(image) 
    display.show()  

def menu25():
    print("menu25 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) 
    draw.text((0, 0), "  ", fill=255) 
    draw.text((0, 20), "   0~9", fill=255)  
    draw.text((0, 40), "-> A~G", fill=255)  
    display.image(image)  
    display.show()  

def menu31():
    print("menu31 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) 
    draw.text((0, 0), "  ", fill=255)  
    draw.text((0, 20), "-> individual 0~9", fill=255)  
    draw.text((0, 40), "   continuous 0~9", fill=255) 
    display.image(image)  
    display.show()  

def menu32():
    global is_running
    print("menu32 is being displayed")
    

    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((0, 0), "  ", fill=255)
    draw.text((0, 20), "   individual 0~9", fill=255)
    draw.text((0, 40), "-> continuous 0~9", fill=255)
    display.image(image)
    display.show()
    
    while True:
        if button_enter.is_pressed:
            while button_enter.is_pressed:
                time.sleep(0.1) 
            is_running = not is_running  
            
            if is_running:
                print("Displaying numbers 0~9 continuously.")
                while is_running:
                    for digit in range(10):
                        if button_enter.is_pressed: 
                            while button_enter.is_pressed:
                                time.sleep(0.1)
                            print("Exiting menu34")
                            is_running = False
                            for pin in segments.values():
                                GPIO.output(pin, GPIO.HIGH)
                            return  
                        
                        display_digit(str(digit))
                        time.sleep(0.5)
            else:
                print("Stopped displaying numbers.")
                for pin in segments.values():
                    GPIO.output(pin, GPIO.HIGH)
                return 


def menu33():
    print("menu33 is being displayed")
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((0, 0), "  ", fill=255)  
    draw.text((0, 20), "-> individual A~G", fill=255)  
    draw.text((0, 40), "   continuous A~G", fill=255)  
    display.image(image)  
    display.show()  

is_running = False  

def menu34():
    global is_running
    print("menu34 is being displayed")
    

    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((0, 0), "  ", fill=255)
    draw.text((0, 20), "   individual A~G", fill=255) 
    draw.text((0, 40), "-> continuous A~G", fill=255) 
    display.image(image)
    display.show()
    
    while True:
        if button_enter.is_pressed:
            while button_enter.is_pressed:
                time.sleep(0.1)  
            is_running = not is_running  
            
            if is_running:
                print("Displaying letters A~G and dp continuously.")
                while is_running:
                    for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'dp']:
                        if button_enter.is_pressed: 
                            while button_enter.is_pressed:
                                time.sleep(0.1)
                            print("Exiting menu34")
                            is_running = False
                            for pin in segments.values():
                                GPIO.output(pin, GPIO.HIGH)
                            return 
                        
                        display_digit(letter)
                        time.sleep(0.5)
            else:
                print("Stopped displaying letters.")
                for pin in segments.values():
                    GPIO.output(pin, GPIO.HIGH)
                return 


def key_scan():
    global key_up
    if key_up:
        if GPIO.input(BTN_UP) == GPIO.LOW:
            key_up = False
            print("Button UP pressed")
            return 4  # Up
        elif GPIO.input(BTN_DOWN) == GPIO.LOW:
            key_up = False
            print("Button DOWN pressed")
            return 3  # Down
        elif GPIO.input(BTN_ENTER) == GPIO.LOW:
            key_up = False
            print("Button ENTER pressed")
            return 1  # Enter
        elif GPIO.input(BTN_EXIT) == GPIO.LOW:
            key_up = False
            print("Button EXIT pressed")
            return 2  # Exit
    if (GPIO.input(BTN_UP) == GPIO.HIGH and
        GPIO.input(BTN_DOWN) == GPIO.HIGH and
        GPIO.input(BTN_ENTER) == GPIO.HIGH and
        GPIO.input(BTN_EXIT) == GPIO.HIGH):
        key_up = True 
        print("All buttons released")

    return 0    


key_table = [
    {'up': 0, 'down': 1, 'enter': 2, 'exit': 0, 'operation': menu11},
    {'up': 0, 'down': 1, 'enter': 5, 'exit': 0, 'operation': menu12},
    {'up': 2, 'down': 3, 'enter': 2, 'exit': 0, 'operation': menu21},
    {'up': 2, 'down': 4, 'enter': 3, 'exit': 0, 'operation': menu22},
    {'up': 3, 'down': 4, 'enter': 4, 'exit': 0, 'operation': menu23},
    {'up': 5, 'down': 6, 'enter': 7, 'exit': 1, 'operation': menu24},
    {'up': 5, 'down': 6, 'enter': 9, 'exit': 1, 'operation': menu25},
    {'up': 7, 'down': 8, 'enter': 7, 'exit': 5, 'operation': menu31},
    {'up': 7, 'down': 8, 'enter': 8, 'exit': 5, 'operation': menu32},
    {'up': 9, 'down': 10, 'enter': 9, 'exit': 6, 'operation': menu33},
    {'up': 9, 'down': 10, 'enter': 10, 'exit': 6, 'operation': menu34},
]

def run_menu():
    global fun_index
    key_input = key_scan()  
    print(f"Current fun_index: {fun_index}")
    if key_input == 4:  # UP
        print(f"Going UP to {key_table[fun_index]['up']}")
        fun_index = key_table[fun_index]['up']
        key_table[fun_index]['operation']()
    elif key_input == 3:  # DOWN
        print(f"Going DOWN to {key_table[fun_index]['down']}")
        fun_index = key_table[fun_index]['down']
        key_table[fun_index]['operation']()
    elif key_input == 1:  # ENTER
        print(f"ENTER pressed at menu {fun_index}")
        fun_index = key_table[fun_index]['enter']
        key_table[fun_index]['operation']()
    elif key_input == 2:  # EXIT
        print(f"EXIT pressed at menu {fun_index}")
        fun_index = key_table[fun_index]['exit']
        key_table[fun_index]['operation']()


    
menu11()

try:
    while True:
        run_menu()
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup() 