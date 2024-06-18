import RPi.GPIO as GPIO
import time
import atexit

LED=12
Vibration=8

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(Vibration,GPIO.IN)

while True:
    if GPIO.input(Vibration):
        GPIO.output(LED,GPIO.HIGH)
    else :
        GPIO.output(LED,GPIO.LOW)
    time.sleep(0.1)
