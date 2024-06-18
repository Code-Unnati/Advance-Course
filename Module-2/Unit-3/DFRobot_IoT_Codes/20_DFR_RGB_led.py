#sudo pip3 install rpi_ws281x
#sudo pip3 install adafruit-circuitpython-neopixel
#sudo python3 -m pip install --force-reinstall adafruit-blinka
#include all neccessary packages to get LEDs to work with Raspberry Pi
import time
import board
import neopixel
import random


#Initialise a strips variable, provide the GPIO Data Pin
#utilised and the amount of LED Nodes on strip and brightness (0 to 1 value)
pixels1 = neopixel.NeoPixel(board.D18, 1, brightness=0.5)

#Also create an arbitary count variable
x=0


while True:
    p1=random.randint(0,255)
    p2=random.randint(0,255)
    p3=random.randint(0,255)
    pixels1.fill((p1, p2, p3))
    time.sleep(0.5)
#    pixels1.fill((255, 0, 100))
#Below demonstrates how to individual address a colour to a LED Node, in this case
#LED Node 10 and colour Blue was selected
#pixels1[10] = (0, 20, 255)

#Sleep for three seconds, You should now have all LEDs showing light with the first node
#Showing a different colour
#time.sleep(4)


#Add a brief time delay to appreciate what has happened    
time.sleep(4)

#Complete the script by returning all the LED to off
pixels1.fill((0, 0, 0))
