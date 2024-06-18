from dfadc import *

board_detect()    # If you forget address you had set, use this to detected them, must have class instance


while board.begin() != board.STA_OK:    # Board begin and check board status
    print_board_status()
    print("board begin faild")
    time.sleep(2)
print("board begin success")

board.set_adc_enable()

while True:
    val = board.get_adc_value(board.A0)   # A0 channels read
    #val = board.get_adc_value(board.A1)   # A1 channels read
    #val = board.get_adc_value(board.A2)   # A2 channels read
    #val = board.get_adc_value(board.A3)   # A3 channels read
#     print("channel: A0, value: %d" %val)
    print("")
    if (val<1900):
        print("Rain Started")
    else:
        print("No Rain")
    
    time.sleep(2)


