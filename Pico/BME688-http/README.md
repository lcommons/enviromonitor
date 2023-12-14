# Raspberry Pi PicoW with BME688 sensor

## Introduction
This MicroPython app runs on a Raspberry Pi PicoW, a small microprocessor with builtin WiFi. It also uses a BME688 enviroment sensor to measure temperature and humidity (other parameters are also available.)
The program implements a basic HTTP web server to serve a display page (for humans), and a data.json response for programs, including the index.html page.