# checkairJS

## Monitoring air quality with a Raspberry Pi

**EDIT: For enviromonitor running on Pi Zero, don't bother with Node.**
**Just use the python3 app and lighttpd.**

This JavaScript app reads air quality data from a Raspeberry pi and then...

1. serves the data from a nodejs server
1. writes the data to a cloud-based RESTful web service.

This app reproduces the functionality of a sibling Python project.

This app runs on a RaspberryPi with one or more sensors attached. The function of this app is to provide access to the data produced by this/these sensors.

### An open question about data storage.

Currently the python app runs every five minutes and writes all data to an AWS database. Is this necessary or ideal? I like have data archived in a resilient robust way that I don't want to have to provide myself. On the other hand, its 90% overkill. Data could be stored locally and then either

- summary data could be written to AWS RDS for long term storage,
- periodically, the local database(s) could be archived in text format to cheaper AWS S3 storage.

The big question: if AWS is just providing emergency backups, how much/long can I store locally? Is it reasonable to store all my data for years and years locally?

### This app adds significant additional capability:

1. read all attached sensors on demand for real-time updates
1. writes to a local Sqllite database for short-term storage, though I will experiment to see how much data can be stored locally. Maybe this can be a daily/weekly/monthly local storage?
1. provide web pages to access the local storage for the sensors attached to this device.

### Architecture

1. A Javascript library (probably a single file) for reading various sensors and returning the results. Consider
   - https://www.npmjs.com/package/ds18b20-raspi
   - other libraries for other sensors
   - need a locally defined list of sensors for this devie
     1. sensorId (e.g. the 64-bit one-wire id of a sensor)
     1. a Label
     1. a description
     1. add date?
1. A nodejs app that provides

   - a REST service for accessing the current and locally stored historical data for the sensors on this device.
     `{"pressure": 1016.197509765625, "temp": 96.14827728271484, "humidity": 55.13484191894531, "pmtwofive": 2.5, "pmten": 7.1, "temp2": 71.15, "timestamp": "2020-08-17T08:25:03.834812"}`
   - a web app that provides human-friendly real time access to current and historical (local) data.
   - https://developerhowto.com/2018/12/29/build-a-rest-api-with-node-js-and-express-js/

1. a Sqlite database for local storage of observations.
   - https://developerhowto.com/2018/12/29/build-a-rest-api-with-node-js-and-express-js/

### Use Cases

1. A Raspberry Pi Zero with a simpe One-Wire temperature sensor, placed in each room to collect hyper-local temperature data.
   - https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/#:~:text=The%20DS18B20%20temperature%20sensor%20is,accurate%20and%20take%20measurements%20quickly.
   - https://www.circuitbasics.com/wp-content/uploads/2016/03/DS18B20-Datasheet.pdf
   - https://www.npmjs.com/package/ds18b20-raspi
   -
1. A Raspberry Pi Zero with a Temperature/Pressure/Humidity sensor for more specialized HVAC control. This might be used to regulate a HRV (heat recovery ventilation) system in a bathroom or for a house.
1. A Raspberry Pi Zero with multiple One-Wire temperature sensors, used to monitor the incoming and ourgoing temperature of a heat exchanger, and control the pump/fan/circulator associated with it.
1. Build out a Raspberry Pi Zero with a One-Wire temp senser.
   - Load SqlLite and store observations locally
   - with CRON, write periodic observations to AWS
   - serve immediate observation
   - serve a user-friendly page of current, recent, and historical data
     - A rest service to serve all the data
     - a web page using AJAX calls to retrieve data and refresh automatically
1. A Heat Recovery Ventilator
   - sits in the bathroom window. The window is open, but the box is sealed tightly.
   - inside intake duct is a PVC pipe open up high to get steam
   - inside exhaust is from the box
   - outside intake and exhaust are PVC elbows pointed down to keep rain out
   - an air filter before air gets into the exchanger
   - two fans: one sucks inside air into the box. The second sucks in outside air and blows into the filter? But that puts the fan out in the cold.

### data_types

#### temp/humidity/pressure/ppm

| id  | name     | description                                                          |
| --- | -------- | -------------------------------------------------------------------- |
| 1   | tempf    | Temperature (fahrenheit)                                             |
| 2   | tempc    | Temperature (celsius)                                                |
| 3   | humidity | Humidity                                                             |
| 4   | pressure | Atmospheric Pressure                                                 |
| 5   | pm2.5    | Particulate matter (smaller than 2.5 microns) concentration in mg/m3 |
| 6   | pm10     | Particulate matter (smaller than 10 microns) concentration in mg/m3  |

#### Locations

| id  | label              |
| --- | ------------------ |
| 1   | living room window |
| 2   | bedroom 1          |
| 3   | bedroom 2          |
| 4   | bathroom 1         |
| 5   | bathroom 2         |
| 6   | kitchen            |

#### Sensors

(Note: need to add a field for the 64-bit ID of each sensor)
|id |label|
|---|-----|
|1| sensehat 2019-11-01
|2| temp sensor DS18B20-1
|3| temp sensor DS18B20-2
|4| temp sensor DS18B20-3
|5| temp sensor DS18B20-4
|6| temp sensor DS18B20-5
|7| temp sensor DS18B20-6

## Setup

1. create user

- sudo adduser airpixx
- sudo adduser airpixx sudo
- sudo passwd airpixx

1. set up wifi

- sudo raspi-config
  - update hostname
  - set wifi stuff

1. install git
   - sudo apt install git
1. install nodejs
   - sudo apt install nodejs
1. install npm
1. npm install express
1. npm install --save ds18b20-raspi
1. git clone https://github.com/lcommons/enviromonitor

On one of the Pi Zeros I had to edit /boot/config.txt to add

`dtoverlay=w1-gpio`

See https://pinout.xyz/pinout/1_wire

## to get node to start on reboot

/etc/rc.local
/full/path/to/myscript.js < /dev/null &

-or-
I think that placing the script in /etc/init.d was the right idea!

Supposed that it was already set executable, the only thing missing was to actually register it with

### run-node

/usr/bin/node ./server.js < /dev/null &

sudo update-rc.d /home/airpixx/enviromonitor/checkairJS/run-node
