from grovepi import * 

from grove_rgb_lcd import * 

import time 

dht_sensor_port = 7 

dht_sensor_type = 0 # 0 for DHT11 and 1 for DHT22 

setRGB(0,255,0) 

while True: 

    [t,h] = dht(dht_sensor_port,dht_sensor_type) 

    print(f"Temp:{t} C Humidity:{h}%") 

    setText_norefresh(f"Temp:{t} C\nHumidity:{h}%") 

    time.sleep(2) 