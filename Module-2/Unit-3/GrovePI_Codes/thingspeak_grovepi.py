#pip3 install thingspeak 

import thingspeak 

import time 

from grovepi import * 

dht_sensor_port = 7 

dht_sensor_type = 0 

channel_id =  '2224094' 

write_key  = 'IN6UY2EWBYPP1173' # PUT YOUR WRITE KEY HERE 


# PUT YOUR WRITE KEY HERE 

  
def measure(channel): 

  try: 

    [ t,h ] = dht(dht_sensor_port,dht_sensor_type) 

    response = channel.update({'field1': t, 'field2': h}) 

    print(f"Temp:{t} C Humidity:{h}%") 

  except: 

    print("connection failed") 

 

channel = thingspeak.Channel(id=channel_id,api_key=write_key) 

while True: 

    measure(channel) # free account has an api limit of 15sec 

    time.sleep(15) 