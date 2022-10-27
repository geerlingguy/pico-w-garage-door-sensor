# Raspberry Pi Pico W Garage Door Sensor

[![Lint](https://github.com/geerlingguy/pico-w-garage-door-sensor/actions/workflows/lint.yml/badge.svg?branch=master)](https://github.com/geerlingguy/pico-w-garage-door-sensor/actions/workflows/lint.yml)

I wanted to build a sensor to determine the state of my garage door—open or closed—and send that state to Home Assistant so I can display the status in a dashboard and build automation from it (e.g. warning me if I'm asleep and the garage door is open!).

If I wanted some sort of cloud integration, I could pay for the kit that connects to my garage door opener, but since [the cloud is just someone else's computer](https://blog.codinghorror.com/the-cloud-is-just-someone-elses-computer/), and I'd rather not rely on some company's weak security to protect data about my home... I want it all local.

## Setting up the Pico W

I decided to use a Raspberry Pi Pico W for this project—you could probably also use an ESP32 or ESP8266 with slight modifications, since this project uses [ESPHome](https://esphome.io).

You will have to flash the firmware to the Pico W in order for it to work.

> **Note**: I also have a MicroPython-based setup in the [`micropython`](pico-w-garage-door-sensor/tree/master/micropython) subdirectory.

### Preparing to flash the Pico W

Before you can flash anything to the Pico W, you have to define a few `secrets` that ESPHome will use when it compiles the program.

Create a `secrets.yaml` file inside this directory, and add the following:

```yaml
---
wifi_ssid: your-wifi-ssid-here
wifi_password: your-wifi-password-here

```

### Using Docker

> **Note**: This will not work until [this Pull Request](https://github.com/esphome/esphome/pull/3284) is merged into ESPHome.

In this directory, I run `docker-compose up -d` to start an esphome container that I'll use to flash the Pico.

Then enter the container:

```
$ docker exec -it esphome bash
root@docker-desktop:/config#
```

This drops you into the container inside the `config` directory, which is shared from this repository.

TODO.

### Using pip source install

For now, until support for the Pico is merged into ESPHome, you have to install the latest dev release with support for the Pico. Make sure you have Python 3 installed on your computer, then run:

```
$ pip3 install git+https://github.com/esphome/esphome.git@dev
```

Make sure your installation is working:

```
$ esphome version
Version: 2022.11.0-dev
```

Then plug in your Pico W, while holding the BOOTSEL button, and when it mounts on your computer, run:

```
$ esphome run garage-door.yml --device /Volumes/RPI-RP2
```

After 20-30 seconds, ESPHome should compile and upload the firmware to the Pico.

> Note: There's also an `led-blink.yml` configuration if you want to upload it quickly to verify `esphome` and your Pico are all wired up correctly. If you `run` that file, it should make your Pico start blinking it's onboard LED 2x per second.
