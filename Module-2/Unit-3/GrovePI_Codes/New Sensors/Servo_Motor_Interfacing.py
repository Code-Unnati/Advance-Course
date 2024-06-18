import RPi.GPIO as GPIO
from dfadc import *
import time
import atexit
atexit.register(GPIO.cleanup)
#GPIO.cleanup()
board_detect()    # If you forget address you had set, use this to detected them, must have class instance

# Set board controler address, use it carefully, reboot module to make it effective

while board.begin() != board.STA_OK:# Board begin and check board status
    print_board_status()
    print("board begin faild")
time.sleep(2)
print("board begin success")

board.set_pwm_enable()                # Pwm channel need external power
board.set_pwm_frequency(50)
board.set_pwm_duty(0,0)
time.sleep(1)
"""
for duty in range(2,17,2):
    board.set_pwm_duty(0,duty)
    time.sleep(2)
"""
while True:
    board.set_pwm_duty(0,2)
    time.sleep(2)
    board.set_pwm_duty(0,15)
    time.sleep(2)
#    board.set_pwm_duty(0,7.0)
#    time.sleep(2)
"""
duty=2
while duty<=17:
    board.set_pwm_duty(0,duty)
    time.sleep(2)
    duty=duty+1
    
board.set_pwm_duty(0,2)
board.set_pwm_duty(0,0)
"""    
#GPIO.cleanup()