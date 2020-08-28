# checkairJS

## Monitoring air quality with a Raspberry Pi

This JavaScript reads air quality data from a Raspeberry pi and then...

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
   - a web app that provides human-friendly real time access to current and historical (local) data.

### Use Cases

1. A Raspberry Pi Zero with a simpe One-Wire temperature sensor, placed in each room to collect hyper-local temperature data.
1. A Raspberry Pi Zero with a Temperature/Pressure/Humidity sensor for more specialized HVAC control. This might be used to regulate a HRV (heat recovery ventilation) system in a bathroom or for a house.
1. A Raspberry Pi Zero with multiple One-Wire temperature sensors, used to monitor the incoming and ourgoing temperature of a heat exchanger, and control the pump/fan/circulator associated with it.
1. Build out a Raspberry Pi Zero with a One-Wire temp senser.
   - Load SqlLite and store observations locally
   - with CRON, write periodic observations to AWS
   - serve immediate observation
   - serve a user-friendly page of current, recent, and historical data
     - A rest service to serve all the data
     - a web page with AJAX calls to retrieve data and refresh automatically
