from dfadc import *

board_detect()

while board.begin() != board.STA_OK:
    print_board_status()
    print("board begin faild")
    time.sleep(2)
print("board begin success")

board.set_adc_enable()

while True:
    val = board.get_adc_value(board.A0)   # A0 channels read
    Temperature = (val/4096)* 3300/10.24
    print("Temperature = %d C" %Temperature)
#    val=val/4096*100
#    print(val)

    time.sleep(2)

