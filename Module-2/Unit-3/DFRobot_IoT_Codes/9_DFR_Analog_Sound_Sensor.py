from dfadc import *
board_detect()
while board.begin() != board.STA_OK:# Board begin and check board status
    print_board_status()
    print("board begin faild")
time.sleep(2)
print("board begin success")

board.set_pwm_enable()                # Pwm channel need external power
board.set_adc_enable()
board.set_pwm_frequency(1000)         # Set frequency to 1000HZ, Attention: PWM voltage depends on independent power supply

while True:
  val = board.get_adc_value(board.A0)
  val = val/4096 *100*5
  print("set all pwm channels duty to %d",val)
  board.set_pwm_duty(0,val)   # Connect DC motor to PWM0
  time.sleep(0.2)

    #print("set part pwm channels duty to 100%")
    
    #board.set_pwm_duty(0, 50)   # Set pwm0 channels duty
    #board.set_pwm_duty(1, 70)  # Set pwm1 channels duty
    #board.set_pwm_duty(2, 80)  # Set pwm2 channels duty
    #board.set_pwm_duty(3, 90)  # Set pwm3 channels duty
    #time.sleep(5)

