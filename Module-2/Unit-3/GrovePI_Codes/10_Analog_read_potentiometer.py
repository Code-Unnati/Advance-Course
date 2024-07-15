import time 

import grovepi 

from grove_rgb_lcd import * 

# Connect the Rotary Angle Sensor to analog port A2 

potentiometer = 2 

time.sleep(1) 

i = 0 

while True: 

    i = grovepi.analogRead(potentiometer) 

    print(i) 

    setRGB(i//4,i//4,i//4) 