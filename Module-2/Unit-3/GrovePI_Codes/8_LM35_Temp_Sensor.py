import time 

import grovepi 

from grove_rgb_lcd import * 

# Connect the LM35 Temp Sensor to analog port A2 
setRGB(255,0,0)
temp_sensor = 2 
time.sleep(1) 
i = 0 
while True: 
    i = grovepi.analogRead(temp_sensor)
    val= i
    print(i)
#    setText_norefresh("Temperature: {0}".format(temp) )