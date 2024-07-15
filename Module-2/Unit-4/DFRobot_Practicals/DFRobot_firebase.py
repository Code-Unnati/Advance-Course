import RPi.GPIO as GPIO
import time
import atexit
from dfadc import *
board_detect()
while board.begin() != board.STA_OK:
    print_board_status()
    print("board begin faild")
    time.sleep(2)
print("board begin success")
board.set_adc_enable()

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BCM)
from time import sleep
from math import isnan
from time import strftime
from firebase import firebase
import math


firebase= firebase.FirebaseApplication('https://diwakartest1-cc222-default-rtdb.firebaseio.com/')
while True:
    # get the temperature and Humidity from the DHT sensor
    temp = board.get_adc_value(board.A0)   # A0 channels read
    humidity = board.get_adc_value(board.A1)
    temperature = (temp/4096)* 100+20
    humidity = (humidity/4096)* 100
    location="Jaipur"
    time_stamp=strftime("%d-%m-%y %H:%M:%S", time.localtime()) #reads the machine time
    t = str(temperature)
    h = str(humidity)
    data={"Location":location,"time_stamp":time_stamp,"Temperature":temperature,"Humidity":humidity}
    print(data)
    result=firebase.post('Weather Station', data)
    print(result)
    sleep(0.5)