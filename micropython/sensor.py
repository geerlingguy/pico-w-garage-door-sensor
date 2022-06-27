import time
from machine import Pin

# Set up variables
check_interval_sec = 0.25
door_sensor = Pin(0, Pin.IN, Pin.PULL_UP)

# Pico LED
led = Pin(25, Pin.OUT)
# Pico W LED
#led = machine.Pin("LED", machine.Pin.OUT)

# Initial value for the sensor
sensor_value = None

# Main loop
while True:
    old_value = sensor_value
    sensor_value = door_sensor.value()

    # Garage door is open.
    if sensor_value == 1:
        if old_value != sensor_value:
            print('Garage door is open.')
        led.on()

    # Garage door is closed.
    elif sensor_value == 0:
        if old_value != sensor_value:
            print('Garage door is closed.')
        led.off()

    time.sleep(check_interval_sec)
