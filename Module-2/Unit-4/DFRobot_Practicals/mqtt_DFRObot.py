#pip install paho-mqtt
# Might not work for python 3(Use Python 2)
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import atexit

LED = 12

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)


def on_connect(client, userdata, flags, rc):
    print("Connected to broker. Return of connection: "+str(rc))

    client.subscribe("MQTTLED")

# Callback - when a message is received
def on_message(client, userdata, msg):
        print("Topic: "+msg.topic+" - Message Received: "+str(msg.payload))
        df=msg.payload.decode('utf-8')
        print(df)

        if (df == "ONLED1"):
          GPIO.output(LED,GPIO.HIGH)
          return 0

        if (df == "OFFLED1"):
          GPIO.output(LED,GPIO.LOW)
          return 0

#main program
client = mqtt.Client()
client.on_connect = on_connect   # configure callback (from when the connection$
client.on_message = on_message   # set callback (from when a message is receive$

client.connect("broker.emqx.io", 1883, 60)

# Endless loop waiting to receive messages. .
client.loop_forever()

