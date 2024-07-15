import smbus
import time
bus = smbus.SMBus(1)

addr = 0x29

CDATAL = 0x94
CDATAH = 0x95
RDATAL = 0x96
RDATAH = 0x97
GDATAL = 0x98
GDATAH = 0x99
BDATAL = 0x9a
BDATAH = 0x9b

while True:
    ClearL = bus.read_byte_data(addr , CDATAL)
    ClearH = bus.read_byte_data(addr , CDATAH)
    Clear = ClearH * 0x100 + ClearL
    print("Clear = 0X%x" %Clear)
    
    RedL = bus.read_byte_data(addr , RDATAL)
    RedH = bus.read_byte_data(addr , RDATAH)
    Red = RedH * 0x100 + RedL
    print("Red   = 0X%x" %Red)
    
    GreenL = bus.read_byte_data(addr , GDATAL)
    GreenH = bus.read_byte_data(addr , GDATAH)
    Green = GreenH * 0x100 + GreenL
    print("Green = 0X%x" %Green)
    
    BlueL = bus.read_byte_data(addr , BDATAL)
    BlueH = bus.read_byte_data(addr , BDATAH)
    Blue = BlueH * 0x100 + BlueL
    print("Blue  = 0X%x" %Blue)
    print(f"R:{Red}, G:{Green}, B:{Blue}, Clear:{Clear}")
    
    print("    ")
    time.sleep(1)

