# pip3 install Pyrebase
from grovepi import *
from grove_rgb_lcd import * 
import time
from math import isnan
from time import strftime
import math
import pyrebase

dht_sensor_port = 7 

dht_sensor_type = 0 # 0 for DHT11 and 1 for DHT22 

setRGB(0,255,0) 

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
        [t,h] = dht(dht_sensor_port,dht_sensor_type)
        print(f"Temp:{t} C Humidity:{h}%")
        setText_norefresh(f"Temp:{t} C\nHumidity:{h}%") 
        print(t)
        print(h)
        data = {"Temperature" : t,"Humidity" : h}
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

