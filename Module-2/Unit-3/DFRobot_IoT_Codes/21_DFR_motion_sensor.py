import RPi.GPIO as GPIO
import time
import atexit

LED=12
PIR=8


atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(PIR,GPIO.IN)

while True:
    if GPIO.input(PIR):
        GPIO.output(LED,GPIO.HIGH)
    else :
        GPIO.output(LED,GPIO.LOW)
    time.sleep(0.1)
