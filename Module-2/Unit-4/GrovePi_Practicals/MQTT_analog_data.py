#pip install paho-mqtt
# Might not work for python 3(Use Python 2)
import paho.mqtt.client as mqtt
from grovepi import *
from grove_rgb_lcd import * 

import time 

dht_sensor_port = 7 

dht_sensor_type = 0 # 0 for DHT11 and 1 for DHT22 

setRGB(0,255,0) 

led = 8

pinMode(led,"OUTPUT")


def on_connect(client, userdata, flags, rc):
    print("Connected to broker. Return of connection: "+str(rc))
    client.subscribe("MQTTLed")

# Callback - when a message is received
def on_message(client, userdata, msg):
        print("Topic: "+msg.topic+" - Message Received: "+str(msg.payload))
        df=msg.payload.decode('utf-8')
        print(df)
#        df3=df.decode()

        if (df == "ONLED1"):
          digitalWrite(led,1)
          return 0

        if (df == "OFFLED1"):
          digitalWrite(led,0)
          return 0


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))

    
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

#main progra6m
        
client = mqtt.Client()
client.on_connect = on_connect   # configure callback (from when the connection$
client.on_message = on_message   # set callback (from when a message is receive$
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.connect("test.mosquitto.org", 1883, 60)

rc = 0
while rc == 0:
    
    rc = client.loop()
    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    [t,h] = dht(dht_sensor_port,dht_sensor_type)
    print(f"Temp:{t} C Humidity:{h}%")
    setText_norefresh(f"Temp:{t} C\nHumidity:{h}%") 
    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.
    if h is not None and t is not None:
      print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
      client.publish("humidity",str(h))
      client.publish("Temp",str(t))
      time.sleep(1)
        
    else:
      print('Failed to get reading. Try again!') 
