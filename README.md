# Kindle weather page

![weatherPageExampl](tabletWeather/weatherPageExample.jpg)

## This project consists of three distinct sub-projects:
1) The Tablet Weather page, shown above. This is a standalone project.
2) A client that runs on a raspberry pi zero or pico (or other microprocessor)
  - serves a static web page served by a webserver running on that pi (lighttpd on Zero, custom server on Pico) which retrieves the JSON file described below
  - Periodically updates a JSON file containing the latest data
  - uses the Mosquitto MQTT client to publish the latest data
  These scripts can read temperature, humidity, air quality, air pressure from a BME688 sensor; temperature from a 1-Wire temperature sensor (based on the DS18B20 sensor chip)
3) Seperately, a centralized server app periodically retrieves MQTT observations and writes those to a RESTful database service

