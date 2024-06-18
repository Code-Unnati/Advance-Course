import RPi.GPIO as GPIO    # Import the python module provided by the Raspberry Pi
import time    # Import time package to control flicker

LED=12       # Define the pin number to which the LED is connected
sensor = 8     # Define the PIN to which the touch sensor is connected

GPIO.setmode(GPIO.BCM)      #Set GPIO mode, BCM mode is common to all RPI 
GPIO.setup(sensor,GPIO.IN)   # Set GPIO12 to output mode
GPIO.setup(LED,GPIO.OUT)     # Set GPIO8 to input mode
GPIO.output(LED,GPIO.HIGH)  #Define LED original value

while True:               #Execute the following commands in an infinite loop
    key = GPIO.input(sensor)
    if (key ):                     # Judge whether the button is pressed
        GPIO.output(LED,GPIO.LOW) #Button pressed, start the micro vibrator
    else :                     # If GPIO8 is low (that is, the button is released), execute the following statement
        GPIO.output(LED,GPIO.HIGH)        # Not start the micro vibrator
time.sleep(0.01)     #Delay one second, here is to control the frequency 
