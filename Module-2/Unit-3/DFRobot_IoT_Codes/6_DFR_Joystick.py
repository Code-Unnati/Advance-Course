import time
import RPi.GPIO as GPIO
import atexit

Button=8

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Button,GPIO.IN)


from dfadc import *

board_detect()    # If you forget address you had set, use this to detected them, must have class instance


while board.begin() != board.STA_OK:    # Board begin and check board status
    print_board_status()
    print("board begin faild")
time.sleep(2)
print("board begin success")

board.set_adc_enable()
  # board.set_adc_disable()

while True:
    X = board.get_adc_value(board.A1)   # A0 channels read
    X = X - 2024
    print("X = %d" %X)
    
    Y = board.get_adc_value(board.A0)   # A0 channels read
    Y = Y - 2024
    print("Y = %d" %Y)
    
    Z = GPIO.input(Button)
    print("Z = %d" %Z)
    print("")

    time.sleep(0.01)
