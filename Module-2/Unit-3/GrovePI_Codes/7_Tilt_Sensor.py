import time
from grovepi import *
import math
LED = 2      #Port for buzzer
Tilt_sensor = 4
pinMode(LED,"OUTPUT")
pinMode(Tilt_sensor,"INPUT")
digitalWrite(LED,0)
while True:
    a=digitalRead(Tilt_sensor)
    print(a)
    if (a==0):
        digitalWrite(LED,0)
    else:
        digitalWrite(LED,1)





