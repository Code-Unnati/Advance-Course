#pip3 install pad4pi
from pad4pi import rpi_gpio

import time

KEYPAD = [

    [1, 2, 3, "A"],

    [4, 5, 6, "B"],

    [7, 8, 9, "C"],

    ["*", 0, "#", "D"]

]

ROW_PINS = [17, 27, 22, 5] # BCM numbering

COL_PINS = [23, 24, 25, 16] # BCM numbering

def print_key(key):

    print(f"Received key from interrupt:: {key}")

try:

    factory = rpi_gpio.KeypadFactory()

    keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS) # makes assumptions about keypad layout and GPIO pin numbers

    keypad.registerKeyPressHandler(print_key)

    print("Press buttons on your keypad. Ctrl+C to exit.")

    while True:

        time.sleep(1)

except KeyboardInterrupt:

    print("Goodbye")

finally:

    keypad.cleanup()

