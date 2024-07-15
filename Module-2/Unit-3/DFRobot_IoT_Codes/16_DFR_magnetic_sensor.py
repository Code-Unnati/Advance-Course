import RPi.GPIO as GPIO    # Import the python module provided by the Raspberry Pi
import time    # Import time package for touch time detection

LED=12          # Define the pin number to which the LED is connected
magnetic_sensor=8           # Define the pin number to which the sensor is connected

GPIO.setmode(GPIO.BCM)        # Set GPIO mode, BCM mode is common to all Raspberry Pi 
GPIO.setup(LED,GPIO.OUT)    # Set GPIO12 to output mode
GPIO.setup(magnetic_sensor,GPIO.IN)    # Set GPIO8 to input mode

while True:        # Execute the following commands in an infinite loop
    if GPIO.input(magnetic_sensor):        # GPIO.input(KEY)will return the state of GPIO and judge, if GPIO8 is high (i.e. The sensor received signal)
         GPIO.output(LED,GPIO.HIGH)      #Set LED signal pin high (Light LED on)
    else :          # If GPIO8 is low (Not receive signal）
     GPIO.output(LED,GPIO.LOW)   #Set LED signal pin low (Turn LED off)
time.sleep(0.1)   # Delay one second 

