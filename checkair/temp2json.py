import json
import requests
from datetime import datetime
import checktemp

'''
This file runs on a raspberry pi with a ds18b20 temperature sensor.
This file has two functions.

getdata 
gets the temperature from a sperate python script that reads the temperature sensor.

writehtml
This function calls getdata, then uses the values from that dict to update
a json file.

Finally, a cron job runs writehtml every minute.
*/1 * * * *  python3 temp2json.py
'''

datadict = {};

def gettempdata(f=True):
   deg_c, deg_f = checktemp.read_temp()
   if (f):
      datadict["temp2"] = deg_f
   else:
      datadict["temp2"] = deg_c

def writehtml():
   jsonPath = "/var/www/html/data.json"
   gettempdata()
   datadict["timestamp"] = datetime.now().isoformat()
   with open(jsonPath,'w') as fp:
      json.dump(datadict, fp)

if __name__ == '__main__':
    writehtml()
