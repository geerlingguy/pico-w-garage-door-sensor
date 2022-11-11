# Raspberry Pi Pico W Garage Door Sensor

[![Lint](https://github.com/geerlingguy/pico-w-garage-door-sensor/actions/workflows/lint.yml/badge.svg?branch=master)](https://github.com/geerlingguy/pico-w-garage-door-sensor/actions/workflows/lint.yml)

I wanted to build a sensor to determine the state of my garage door—open or closed—and send that state to Home Assistant so I can display the status in a dashboard and build automation from it (e.g. warning me if I'm asleep and the garage door is open!).

If I wanted some sort of cloud integration, I could pay for the kit that connects to my garage door opener, but since [the cloud is just someone else's computer](https://blog.codinghorror.com/the-cloud-is-just-someone-elses-computer/), and I'd rather not rely on some company's weak security to protect data about my home... I want it all local.

## Garage Door sensors

The actual sensors I use are the ['Enforcer' (model SM-4201-LQ) from Seco-Larm](https://amzn.to/3hD2uGc). I chose these because they are rugged and purpose-built for mounting to garage door tracks.

Watch [this video](https://youtu.be/dFDGtlSi9Eg?t=459) to see how I installed the sensors on my garage doors, and how I wired them to the Pico W.

![RPi Pico Breakout Board wired to garage door sensor](/images/rpi-pico-breakout-pins.jpg)

I used a [RPi Pico Breakout board](https://amzn.to/3O3wFT8) mounted directly to my garage wall, and wired one wire of each sensor to ground, and the `east_garage_door` sensor's other wire to GPIO pin 2.

You can pick any GPIO connection, though—just change the appropriate lines inside `garage-door.yml` before flashing the Pico W using the instructions below.

## Flashing the Pico W

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
ota_password: choose-an-ota-password
api_password: choose-an-api-password
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

Compile the binary for the garage door sensor:

```
$ esphome compile garage-door.yml
```

Copy the generated binary into the current directory:

```
$ cp .esphome/build/rpi-pico/.pioenvs/rpi-pico/firmware.uf2 ./rpi-pico.uf2
```

Then on your host computer, with the Pico W booted into BOOTSEL mode (hold down the BOOTSEL button while plugging in the USB cable), copy the `rpi-pico.uf2` file over to the Pico W. When the copy is complete, the Pico should reboot and start working as a garage door sensor.

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

> On Raspberry Pi or other Linux devices, the `--device` should be `/dev/sda1` (or whatever mount point)

After 20-30 seconds, ESPHome should compile and upload the firmware to the Pico.

> Note: There's also an `led-blink.yml` configuration if you want to upload it quickly to verify `esphome` and your Pico are all wired up correctly. If you `run` that file, it should make your Pico start blinking it's onboard LED 2x per second.

### Installation from a Raspberry Pi

If you are using a Raspberry Pi, first install Pip:

```
sudo apt install python3-pip git
```

Then follow the directions above for 'Using pip source install'.

#### First time install

For now, if you're not running things on a Mac at least, the first install must be done by copying a manually-downloaded .uf2 file to the Pico in BOOTSEL mode.

After ensuring `esphome` installed (see 'Using pip source install' above):

  1. Run `esphome dashboard ./`
  2. In a browser, visit the Pi's IP address at port `:6052`
  3. Click the three dots next to the project
  4. Click 'Install'
  5. Click 'Manual download'
  6. Click the link and wait for the download to be generated, then click the Download link.

Copy the downloaded `rpi-pico.uf2` file to the Pico's filesystem while it's in BOOTSEL mode (hold down BOOTSEL while plugging it in). Unplug and replug the Pico.

### Debugging with ESPHome

If you want to see debug output, after the first time you flash the Pico, you can change the `run` command to:

```
$ esphome run led-blink.yml --device /dev/tty.usbmodem2101
```

And it will compile ESPHome, load it onto the Pico, and start displaying logged output. You can change the [log level](https://esphome.io/components/logger.html) using the `logger.level` setting.
