# TODO: SEE https://forums.raspberrypi.com/viewtopic.php?p=2014658#p2014658

import network
import socket
import time

from machine import Pin
import uasyncio as asyncio

check_interval_sec = 0.25
door_sensor = Pin(0, Pin.IN, Pin.PULL_UP)
led = machine.Pin("LED", machine.Pin.OUT, value=1)

# Configure your WiFi SSID and password
ssid = 'TODO'
password = 'TODO'

# Initial value for the sensor
sensor_value = None

wlan = network.WLAN(network.STA_IF)

html = """<!DOCTYPE html>
<html>
    <head> <title>Garage Door Status</title> </head>
    <body> <h1>Garage Door Status</h1>
        <p>Garage door is currently TODO.</p>
    </body>
</html>
"""


def connect_to_wifi():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Diable powersave mode
    wlan.connect(ssid, password)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        blink_led(0.2, 5)
        raise RuntimeError('wifi connection failed')
    else:
        blink_led(1, 2)
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


def blink_led(frequency = 0.5, num_blinks = 3):
    for i in range(num_blinks):
        led.on()
        time.sleep(frequency)
        led.off()
        time.sleep(frequency)


async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
    writer.write(html)
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")


def sensor_update():
    while True:
        global sensor_value

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


async def main():
    print('Connecting to WiFi...')
    connect_to_wifi()

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

    while True:
        print("Monitoring garage door state....")
        sensor_update()
        await uasyncio.sleep(check_interval_sec)


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
