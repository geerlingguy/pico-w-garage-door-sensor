import time
from machine import Pin

led = Pin("LED", Pin.OUT, value=1)

while True:
    led.toggle()
    time.sleep(0.5)
    led.toggle()
    time.sleep(0.5)
