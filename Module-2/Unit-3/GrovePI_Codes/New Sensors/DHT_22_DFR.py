#pip3 install adafruit-circuitpython-dht
#sudo apt install gpiod
## Can check installed library using  apt show libgpiod2
import time
import adafruit_dht
import board

dht_device = adafruit_dht.DHT22(board.D4)

while True:
    try:
        temperature_c = dht_device.temperature
        temperature_f = temperature_c * (9 / 5) + 32

        humidity = dht_device.humidity

        print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))
    except RuntimeError as err:
        print(err.args[0])

    time.sleep(2.0)