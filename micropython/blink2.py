import machine
import time
import network
import utime

led = machine.Pin('LED', machine.Pin.OUT)

while (True):
    led.on()
    time.sleep(.2)
    led.off()
    time.sleep(.2)
   