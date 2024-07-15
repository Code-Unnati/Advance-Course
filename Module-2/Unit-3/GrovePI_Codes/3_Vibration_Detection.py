import time
from grovepi import *
import math
buzzer_pin = 2      #Port for buzzer
vibration_sensor = 4
pinMode(buzzer_pin,"OUTPUT")
pinMode(vibration_sensor,"INPUT")
digitalWrite(buzzer_pin,0)
while True:
    a=digitalRead(vibration_sensor)
    print(a)
    if (a==0):
        digitalWrite(buzzer_pin,0)
    else:
        digitalWrite(buzzer_pin,1)

