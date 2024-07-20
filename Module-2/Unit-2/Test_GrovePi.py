import time​

from grovepi import *​

digital_ports = [2, 3, 4, 5, 6, 7, 8]​

def check_digital_ports():​

    for port in digital_ports:​

        try:​

            pinMode(port, "OUTPUT")​

            digitalWrite(port, 1)​

            time.sleep(1)​

            state = digitalRead(port)​

            print(f"Digital Port {port} - HIGH state: {state}")​

            digitalWrite(port, 0)​

            time.sleep(1)​

            state = digitalRead(port)​

            print(f"Digital Port {port} - LOW state: {state}")​

        except IOError:​

            print(f"Error reading/writing Digital Port {port}")