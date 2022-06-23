import time

led = machine.Pin("LED", machine.Pin.OUT, value=1)

while True:
    led.toggle()
    time.sleep(0.5)
    led.toggle()
    time.sleep(0.5)