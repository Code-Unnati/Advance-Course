import RPi.GPIO as GPIO
import time

# pir at BCM port 23
# PIR sensitivity (detect  range) can be tuned by adjusting the
# screw on the right side of the buuzzer
pir_gpio = 23
LED=12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_gpio, GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
def no_motion():
    print("Nothing moves â€¦")
    GPIO.output(LED,GPIO.LOW)

def motion_detected():
    print("Motion detected at "+str(time.ctime()))
    GPIO.output(LED,GPIO.HIGH)

try:
  while True:
    GPIO.output(LED,GPIO.LOW)  
    if(GPIO.input(pir_gpio) == 0):
        no_motion()
    elif(GPIO.input(pir_gpio) == 1):
        motion_detected()
    time.sleep(0.1)
except KeyboardInterrupt:
  print('interrupted!')
  GPIO.cleanup()