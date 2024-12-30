import time
import board
import RPi.GPIO as GPIO
import busio

segments = {
    'a': 25, 'b': 5, 'c': 6, 'd': 12, 'e': 13, 'f': 14, 'g': 15, 'x': 16, 'dp': 19,
    '1': 20, '2': 21, '3': 26
}


GPIO.setmode(GPIO.BCM)
for segment in segments.values():
    GPIO.setup(segment, GPIO.OUT, initial=GPIO.LOW)

digit_map = {
    '0': ['a', 'b', 'c', 'd', 'e', 'f'],
    '1': ['b', 'c'],
    '2': ['a', 'b', 'd', 'e', 'g'],
    '3': ['a', 'b', 'c', 'd', 'g'],
    '4': ['b', 'c', 'f', 'g'],
    '5': ['a', 'c', 'd', 'f', 'g'],
    '6': ['a', 'c', 'd', 'e', 'f', 'g'],
    '7': ['a', 'b', 'c'],
    '8': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    '9': ['a', 'b', 'c', 'd', 'f', 'g'],
}


def display_digit(digit):
    for pin in segments.values():
        GPIO.output(pin, GPIO.LOW)
    
    segments_state = digit_map[digit]
    for segment in segments_state:
        GPIO.output(segments[segment], GPIO.HIGH)


def run_auto_display():
    print("Displaying numbers 0~9 continuously.")
    while True:  
        for digit in range(10):
            display_digit(str(digit)) 
            time.sleep(0.5) 

try:
    run_auto_display() 
except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup() 
