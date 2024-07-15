# 2022 Adesola Samuel
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
import pyrebase

config = {
  "apiKey": "AIzaSyBLCJBhKJ6Gi1HN3QkqTqvlklMfdf8vBL4",
  "authDomain": "diwakarrpi.firebaseapp.com",
  "databaseURL": "https://diwakarrpi-default-rtdb.firebaseio.com/",
  "storageBucket": "diwakarrpi.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()




while True:
    try:
        # Print the values to the serial port
        temp = board.get_adc_value(board.A0)   # A0 channels read
        humidity = board.get_adc_value(board.A1)
        temperature = (temp/4096)* 100+20
        humidity = (humidity/4096)* 100
        print(temperature)
        print(humidity)
        data = {"Temperature" : temperature,"Humidity" : humidity}
        db.child("Status").push(data)
        db.update(data)
        print("Sent to Firebase")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

