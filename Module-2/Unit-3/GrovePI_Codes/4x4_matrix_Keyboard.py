import RPi.GPIO as GPIO
import time
"""
R1=4
R2=5
R3=6
R4=7
C1=8
C2=9
C3=10
C4=11
"""
"""
R1=5
R2=6
R3=13
R4=19
C1=12
C2=16
C3=20
C4=21
"""
R1=17
R2=27
R3=22
R4=5
C1=23
C2=24
C3=25
C4=16

GPIO.setmode(GPIO.BCM)
GPIO.setup(R1,GPIO.OUT)
GPIO.setup(R2,GPIO.OUT)
GPIO.setup(R3,GPIO.OUT)
GPIO.setup(R4,GPIO.OUT)

GPIO.setup(C1,GPIO.IN)
GPIO.setup(C2,GPIO.IN)
GPIO.setup(C3,GPIO.IN)
GPIO.setup(C4,GPIO.IN)



def readLine(line, characters):
    
    GPIO.output(line,GPIO.HIGH)
    
    if(GPIO.input(C1) == 1):
        print(characters[0])
    if(GPIO.input(C2) == 1):
        print(characters[1])
    if(GPIO.input(C3) == 1):
        print(characters[2])
    if(GPIO.input(C4) == 1):
        print(characters[3])

    GPIO.output(line,GPIO.LOW)


while True:
    
    readLine(R1, ["1","2","3","A"])

    readLine(R2, ["4","5","6","B"])

    readLine(R3, ["7","8","9","C"])

    readLine(R4, ["*","0","#","D"])

    time.sleep(0.1)



print("\nApplication stopped!")


