from lcddf import *
setText("Hello world\nThis is an LCD test")
setRGB(0,128,64)
time.sleep(2)
for c in range(0,255):
    setText_norefresh("Going to sleep in {}...".format(str(c)))
    setRGB(c,255-c,0)
    time.sleep(0.3)
setRGB(0,255,0)
setText("Bye bye, this should wrap onto next line")
setText("Great, this ")
