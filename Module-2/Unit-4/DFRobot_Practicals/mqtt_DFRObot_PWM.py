#pip install paho-mqtt
# Might not work for python 3(Use Python 2)
import paho.mqtt.client as mqtt
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
board.set_pwm_enable()  
board.set_pwm_frequency(1000)      
LED = 12

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)


def on_connect(client, userdata, flags, rc):
    print("Connected to broker. Return of connection: "+str(rc))
    client.subscribe("Motor")

# Callback - when a message is received
def on_message(client, userdata, msg):
        print("Topic: "+msg.topic+" - Message Received: "+str(msg.payload))
        df=msg.payload.decode('utf-8')
        print(df)
        print(type(df))
        df=int(df)
#        df3=df.decode()

#        if (df == 100):
#          board.set_pwm_duty(0,df)
#          return 0

#        if (df == 50):
#          board.set_pwm_duty(0,df)
#          return 0
        
#        if (df == 10):
        board.set_pwm_duty(0,df)
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
client.connect("broker.emqx.io", 1883, 60)

rc = 0
while rc == 0:
    
    rc = client.loop()
    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    temp = board.get_adc_value(board.A0)   # A0 channels read
    humidity = board.get_adc_value(board.A1)
    temperature = (temp/4096)* 100+20
    humidity = (humidity/4096)* 100
#    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.
    if humidity is not None and temperature is not None:
      print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
      client.publish("humidity",str(humidity))
      client.publish("Temp",str(temperature))
      time.sleep(1)
        
    else:
      print('Failed to get reading. Try again!') 

