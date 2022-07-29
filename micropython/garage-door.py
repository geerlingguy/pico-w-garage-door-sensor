import time
import network
import utime

from machine import Pin
import uasyncio as asyncio

check_interval_sec = 0.25
door_sensor = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT, value=1)
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
ledGreen = Pin(4, Pin.OUT)
ledRed = Pin(5, Pin.OUT)

chars = [
    [0,0,0,0,0,0,0,0],#0
    [1,1,1,0,0,1,1,1],#1
    [0,1,0,0,1,0,0,0],#2
    [0,1,0,0,0,0,1,0],#3
    [0,0,1,0,0,1,1,0],#4
    [0,0,0,1,0,0,1,0],#5
    [0,0,0,1,0,0,0,0],#6
    [1,1,0,0,0,1,1,1],#7
    [0,0,0,0,0,0,0,0],#8
    [0,0,0,0,0,0,1,0],#9
    [0,1,1,1,1,1,1,1],#Open
    [0,1,1,0,0,1,1,0],#Closed
]

def clear():
    for i in pins:
        i.value(1)
clear()

""" while True:
    for i in range(len(chars)):
        for j in range(len(pins)):
            pins[j].value(chars[i][j])
            utime.sleep(1) """

# Configure your WiFi SSID and password
ssid = 'Tecnoadsl_Gramigna'
password = 'puravida'

# Initial value for the sensor
sensor_value = None

wlan = network.WLAN(network.STA_IF)


def get_html(garage_door_status = "OPEN"):
    html = """<!DOCTYPE html>
    <html>
        <head>
            <title>Garage Door Status</title>
            <meta http-equiv="refresh" content="1">
        </head>
        <body> <h1>Garage Door Status</h1>
            <p>Garage Door is currently $status. </p>
        </body>
    </html>
    """
    return html.replace("$status", garage_door_status)


def blink_led(frequency = 0.5, num_blinks = 3):
    for _ in range(num_blinks):
        led.on()
        time.sleep(frequency)
        led.off()
        time.sleep(frequency)


async def connect_to_wifi():
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
        blink_led(0.1, 10)
        raise RuntimeError('WiFi connection failed')
    else:
        blink_led(0.5, 2)
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


async def serve_client(reader, writer):
    global sensor_value

    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

    if sensor_value:
        writer.write(get_html('OPEN'))
    else:
        writer.write(get_html('CLOSED'))

    await writer.drain()
    await writer.wait_closed()


def sensor_update():
    global sensor_value

    old_value = sensor_value
    sensor_value = door_sensor.value()
    clear()
    # Garage door is open.
    if sensor_value == 1:
        if old_value != sensor_value:
            print('Garage door is open.')
        
        clear()
        led.on()
        ledRed.on()
        ledGreen.off()
        pins[0].value(chars[0][0])
        pins[2].value(chars[6][5])
        pins[3].value(chars[6][5])
        pins[4].value(chars[6][5])
        pins[5].value(chars[6][5])
        pins[6].value(chars[6][5])
        # pins[j].value(chars[i][j]) 

    # Garage door is closed.
    elif sensor_value == 0:
        if old_value != sensor_value:
            print('Garage door is closed.')
        clear()
        led.off()
        ledRed.off()
        ledGreen.on()
        pins[0].value(chars[0][0])
        pins[2].value(chars[6][5])
        pins[5].value(chars[6][5])
        pins[6].value(chars[6][5])


async def main():
    print('Connecting to WiFi...')
    asyncio.create_task(connect_to_wifi())

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

    print("Monitoring garage door state....")
    while True:
        sensor_update()
        await asyncio.sleep(check_interval_sec)


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
