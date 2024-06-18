from dfadc import *

board_detect()    # If you forget address you had set, use this to detected them, must have class instance


while board.begin() != board.STA_OK:    # Board begin and check board status
    print_board_status()
    print("board begin faild")
    time.sleep(2)
print("board begin success")

board.set_adc_enable()

while True:
    humidity = board.get_adc_value(board.A0)   # A0 channels read
    humid = (humidity/4096)* 100
    sf=f"Humidity = {humid} %"
    print(sf)
    print("")

    time.sleep(2)

