import time 

import grovepi 

from grove_rgb_lcd import * 

# Connect the Grove Light Sensor to analog port A0 

# SIG,NC,VCC,GND 

light_sensor = 0 

 

# Connect the LED to digital port D4 

# SIG,NC,VCC,GND 

led = 5 

 

# Turn on LED once sensor exceeds threshold resistance 

threshold = 100

 

grovepi.pinMode(light_sensor,"INPUT") 

grovepi.pinMode(led,"OUTPUT") 

 

while True: 

    try: 

        # Get sensor value 

        sensor_value = grovepi.analogRead(light_sensor) 

        print(sensor_value) 

 

        # Calculate resistance of sensor in K 

        resistance = (float)(1023 - sensor_value) * 10 / (sensor_value + 0.001) 

        setRGB(255-10*sensor_value,255-10*sensor_value,255-10*sensor_value) 

 

        if sensor_value > threshold: 

            # Send HIGH to switch on LED 

            grovepi.digitalWrite(led,0) 

            setText_norefresh("Turn off Smart Light") 

        else: 

            # Send LOW to switch off LED 

            grovepi.digitalWrite(led,1) 

            setText_norefresh("Turn on Smart Light") 

 

        print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance)) 

        time.sleep(.5) 

 

    except IOError: 

        print ("Error") 