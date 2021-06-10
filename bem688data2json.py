import glob
import time

import json
import requests
from datetime import datetime

import board
import adafruit_bme680


'''
This file runs on a raspberry pi with a Busch BEM688 temerature/humidity/gas sensor.
This file has two sets of functions.

read_temp and read_temp_raw 
reads the temperature sensor.

writehtml
This function calls read_temp, then uses the values from that dict to update
a json file.

Finally, a cron job runs writehtml every minute.
*/1 * * * *  python3 /home/airpiXX/temp2json.py
'''

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'

i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

def read_data():
    print('Temperature: {} degrees C'.format(sensor.temperature))
    print('Gas: {} ohms'.format(sensor.gas))
    print('Humidity: {}%'.format(sensor.humidity))
    print('Pressure: {}hPa'.format(sensor.pressure))
    print(sensor.humidity)
    temp = sensor.temperature * 9.0 / 5.0 + 32.0
    humidity = sensor.humidity * 1.00
    pressure = sensor.pressure
    gas = sensor.gas
    return temp, humidity, pressure, gas

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


datadict = {}


def gettempdata(f=True):
    deg_c, deg_f = read_temp()
    if (f):
        datadict["temp2"] = deg_f
    else:
        datadict["temp2"] = deg_c

def getJsonData():
    temp, humidity, pressure, gas = read_data();
    if (temp):
        datadict["temp"] = temp
    if (humidity):
        datadict["humidity"] = humidity
    if (pressure):
        datadict["pressure"] = pressure
    if (gas):
        datadict["gas"] = gas

def writejson():
    jsonPath = "/var/www/html/data.json"
    getJsonData()
    datadict["timestamp"] = datetime.now().isoformat()
    with open(jsonPath, 'w') as fp:
        json.dump(datadict, fp)

def writehtml():
    jsonPath = "/var/www/html/data.json"
    gettempdata()
    datadict["timestamp"] = datetime.now().isoformat()
    with open(jsonPath, 'w') as fp:
        json.dump(datadict, fp)


if __name__ == '__main__':
    writejson()
