import tweepy
from grovepi import *
from grove_rgb_lcd import * 
import time
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
dht_sensor_port = 7 

dht_sensor_type = 0 # 0 for DHT11 and 1 for DHT22 
setRGB(0,255,0) 
while True:
    # Print the values to the serial port
    [t,h] = dht(dht_sensor_port,dht_sensor_type)
    print(f"Temp:{t} C Humidity:{h}%")
    setText_norefresh(f"Temp:{t} C\nHumidity:{h}%") 
    print(t)
    print(h)
    time_stamp=strftime("%d-%m-%y %H:%M:%S", time.localtime())
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
    sd='Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h)
    sd=time_stamp+" "+sd
    print(sd)
    client.create_tweet(text=sd)
    print("Sent to Twitter")
    time.sleep(5.0)