import time
from grovepi import *
import math
buzzer_pin = 2      #Port for buzzer
button = 4
pinMode(buzzer_pin,"OUTPUT")
pinMode(button,"INPUT")
digitalWrite(buzzer_pin,0)
while True:
    a=digitalRead(button)
    print(a)
    if (a==0):
        digitalWrite(buzzer_pin,0)
    else:
        digitalWrite(buzzer_pin,1)
