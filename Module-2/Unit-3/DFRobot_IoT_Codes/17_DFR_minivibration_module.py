import RPi.GPIO as GPIO
import time
import atexit

vibration_module=12
Button=8

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BCM)
GPIO.setup(vibration_module,GPIO.OUT)
GPIO.setup(Button,GPIO.IN)

while True:
    if GPIO.input(Button):
        GPIO.output(vibration_module,GPIO.HIGH)
    else :
        GPIO.output(vibration_module,GPIO.LOW)
    time.sleep(0.1)
