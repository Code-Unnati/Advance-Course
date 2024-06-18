from grovepi import *

led = 7
pinMode(led,"OUTPUT")

ip = input()
if ip == "H":
  digitalWrite(led,1)
elif ip =="L":
  digitalWrite(led,0)

