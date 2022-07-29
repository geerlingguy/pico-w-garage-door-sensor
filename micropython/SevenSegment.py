import machine
import time
import network
import utime
import uasyncio as asyncio

led = machine.Pin('LED', machine.Pin.OUT)
pins = [
    Pin(16,Pin.OUT),#middle
    Pin(17,Pin.OUT),#topLeft
    Pin(18,Pin.OUT),#top
    Pin(19,Pin.OUT),#topRight
    Pin(13,Pin.OUT),#bottomRight
    Pin(14,Pin.OUT),#bottom
    Pin(15,Pin.OUT),#bottonLeft
    Pin(12,Pin.OUT)#dot
      ]
while (True):
    led.on()
    time.sleep(.2)
    led.off()
    time.sleep(.2)
   