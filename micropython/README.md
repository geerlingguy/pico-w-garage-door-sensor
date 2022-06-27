# MicroPython Pico W Garage Door Sensor

Because ESPHome wasn't quite ready prior to launch day, I also created some code for the Pico W to run my garage door sensor strictly using MicroPython.

## Getting Started

This directory contains a file named `garage-door.py`. This file contains the code you'll need to flash to your Pico W to get it to work.

But before that, please follow the [Getting started with Raspberry Pi Pico](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico) guide—you should end up with Thonny installed and have the MicroPython firmware on the Pico.

Besides the Garage Door Sensor file, I've included other examples for getting started:

  - `led-blink.py`: Helpful for ensuring you have your environment set up correctly. Run it on the Pico W, and the LED should blink once per second.
  - `sensor.py`: Simple example for testing a magnetic reed sensor local on the Pico W itself. You can use this to ensure you have the circuit wired properly. The LED should be lit when the sensor is 'open' (the magnet is far away), and should be off when the sensor is 'closed' (the magnet is close).
  - `webserver.py`: A lightweight MicroPython webserver example.

## Customizing the Code

Open the `garage-door.py` file in Thonny.

To get it on the Pico W, you can choose File > Save As... then choose 'Raspberry Pi Pico' as the location to save it. Save it as `garage-door.py`.

Now, TODO.
