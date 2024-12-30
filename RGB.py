import time
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 16        
LED_PIN = 18                
LED_FREQ_HZ = 800000       
LED_DMA = 10              
LED_BRIGHTNESS = 255       
LED_INVERT = False        
LED_CHANNEL = 0           

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()               

def rgb_gradient():
    red = 255
    green = 0
    blue = 0

    while True:
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

try:
    rgb_gradient()

except KeyboardInterrupt: 
    strip.setBrightness(0)
    strip.show()
    print("Program terminated")
