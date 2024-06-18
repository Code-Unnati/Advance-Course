import tweepy
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
import math

consumer_key = '2IWlVt3Px1GtUfM7T6n1thTGC'
consumer_secret = 'YasyTDfoMXRakvxLWLtyVXatC98T8lTIXdy96kiZyT7ClgXGad'
access_token = '1043489874559397888-Ok5ZP06n6kaPIHHrgSk41fIhJPfArK'
access_token_secret = 'gFmwTsr9lH7b5v8t8BR8mTpDwyJ7M7GttYMu4UL4zm6cz'

client = tweepy.Client(consumer_key=consumer_key,consumer_secret=consumer_secret,access_token=access_token,access_token_secret=access_token_secret)

location="Jaipur"
#time_stamp=strftime("%d-%m-%y %H:%M:%S", time.localtime())
#print(time_stamp)

while True:
    # Print the values to the serial port
    temp = board.get_adc_value(board.A0)   # A0 channels read
    humidity = board.get_adc_value(board.A1)
    temperature = (temp/4096)* 100+20
    humidity = (humidity/4096)* 100
    print(temperature)
    print(humidity)
    time_stamp=strftime("%d-%m-%y %H:%M:%S", time.localtime())
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    sd='Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
    sd=time_stamp+" "+sd
    print(sd)
    client.create_tweet(text=sd)
    print("Sent to Twitter")
    time.sleep(5.0)