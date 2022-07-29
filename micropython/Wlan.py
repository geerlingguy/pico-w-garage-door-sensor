# import network
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect("Tecnoadsl_Gramigna","puravida")
# print(wlan.isconnected())
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = "Tecnoadsl_Gramigna"
pw = "puravida"

wlan.connect(ssid, pw)

def light_onboard_led():
    led = machine.Pin('LED', machine.Pin.OUT)
    led.on()
    time.sleep(.2)
    led.off()
    time.sleep(.2);

timeout = 10
while timeout > 0:
    if wlan.status() >= 3:
        light_onboard_led()
        timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)
   
wlan_status = wlan.status()
