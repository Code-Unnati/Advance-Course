from grove_rgb_lcd import * 

import time 

import random 

while True: 

    p1=random.randint(0,255) 

    p2=random.randint(0,255) 

    p3=random.randint(0,255) 

    time.sleep(0.5) 

    setRGB(p1,p2,p3) # (Green) RGB Pattern 

 

    setText("Hi Welocme to Code Unnati") 