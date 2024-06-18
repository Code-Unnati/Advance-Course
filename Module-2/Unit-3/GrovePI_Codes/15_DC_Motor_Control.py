import time
import grovepi
from grove_rgb_lcd import *
# Connect the Rotary Angle Sensor to analog port A2
potentiometer = 2

# Connect the dc_motor to digital port D5
# Check for PWM pin
dc_motor = 5

grovepi.pinMode(dc_motor,"OUTPUT")
time.sleep(1)
i = 0

while True:
    try:
        # Read resistance from Potentiometer
        i = grovepi.analogRead(potentiometer)
        print(i)

        # Send PWM signal to dc_motor
        grovepi.analogWrite(dc_motor,i//4)
        setRGB(i//4,i//4,i//4)

    except IOError:
        print("Error")

