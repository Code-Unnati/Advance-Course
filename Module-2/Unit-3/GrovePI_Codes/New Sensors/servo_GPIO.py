# Raspberry Pi + MG90S Servo PWM Control Python Code
#
#
import RPi.GPIO as GPIO
import time

# setup the GPIO pin for the servo
servo_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)

# setup PWM process
pwm = GPIO.PWM(servo_pin,50) # 50 Hz (20 ms PWM period)

pwm.start(7) # start PWM by rotating to 90 degrees


while True:
    pwm.ChangeDutyCycle(2.0) # rotate to 0 degrees
    time.sleep(0.5)
    pwm.ChangeDutyCycle(12.0) # rotate to 180 degrees
    time.sleep(0.5)
    pwm.ChangeDutyCycle(7.0) # rotate to 90 degrees
    time.sleep(0.5)


pwm.ChangeDutyCycle(0) # this prevents jitter
pwm.stop() # stops the pwm on 13
GPIO.cleanup() # good practice when finished using a pin  """