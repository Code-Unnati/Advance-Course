from dfadc import *
import thingspeak
import time
board_detect()
channel_id =  '2465172'
write_key  = 'VJMU8L2I7EWO13LK' # PUT YOUR WRITE KEY HERE
while board.begin() != board.STA_OK:
    print_board_status()
    print("board begin faild")
    time.sleep(2)
print("board begin success")

board.set_adc_enable()
channel = thingspeak.Channel(id=channel_id,api_key=write_key)
while True:
    temp = board.get_adc_value(board.A0)   # A0 channels read
    humidity = board.get_adc_value(board.A1)
    temperature = (temp/4096)* 100+20
    humid = (humidity/4096)* 100
#    print("Temperature = %d C" %Temperature)
#    val=val/4096*100
    print(temperature)
    print(humid)
    response = channel.update({'field1': temperature, 'field2': humid})

    time.sleep(2)
