import RPi.GPIO as GPIO
import time
import atexit

LED=12

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)

while True:
    GPIO.output(LED,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED,GPIO.LOW)
    time.sleep(1)
