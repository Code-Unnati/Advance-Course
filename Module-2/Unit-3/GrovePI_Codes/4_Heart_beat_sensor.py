import time
from grovepi import *
import math
LED = 2      #Port for buzzer
heart_beat_sensor = 4
pinMode(LED,"OUTPUT")
pinMode(heart_beat_sensor,"INPUT")
digitalWrite(LED,0)
while True:
    a=digitalRead(heart_beat_sensor)
    print(a)
    if (a==0):
        digitalWrite(LED,0)
    else:
        digitalWrite(LED,1)


