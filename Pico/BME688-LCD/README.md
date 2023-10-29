# Raspberry Pi Pico, BME-688 sensor, 16x2 LCD display

## Introduction
This project uses a Raspberry Pi Pico microcontroller running MicroPython, a BME-688 sensor to measuer temperature, hunmidity, pressure, and air quality. It uses a basic 16x2 LCD display. The intended use case is a small package running off a (solar-charged) battery so low power consumption is a priority. The Pico and the LCD were chosen for this reason.

## To Do?
every 5(?) minutes, save the data to local storage
If the Pico is WIFI enabled, access via SSH
If NOT WIFI-enabled, just shut the thing down, pull out the SD card, and stick it in a reader to copy the files.

