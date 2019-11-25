import pymysql
import serial
import json
import requests
from datetime import datetime
from sense_hat import SenseHat
'''
This file runs on a raspberry pi with a sense hat AND an air quality sensor.
This file has two functions.

getdata 
gets enviromental data from the sense hat and also reads air quality 
data from a serial port.

writehtml
This function calls getdata, then uses the values from that dict to update
the sample content string and writes that to /var/www/html/index.html.

Finally, a cron job runs writehtml every five minutes.
*/5 * * * *  python3 checkair.py
'''


def getdata():
    sense = SenseHat()
    sense.clear()
    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    temp = 9.0/5.0 * temp + 32
    humidity = sense.get_humidity()
    #print("humidity: ", humidity)
    #print("temp : ", temp)
    #print("pressure: ", pressure)
    
    data = []
    ser = serial.Serial('/dev/ttyUSB0')
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)
        
    #print("data: ",data)
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
        
    #print("pmtwofive: ", pmtwofive)
    #print("pmten: ", pmten)

    datadic = {};
    datadic["pressure"] = pressure
    datadic["temp"] = temp
    datadic["humidity"] = humidity
    datadic["pmtwofive"] = pmtwofive
    datadic["pmten"] = pmten

    return datadic

def writehtml():
    path = "/var/www/html/index.html"
    
    data = getdata()
    #print("getdata: ",data)
    newhtmlstring = htmlstring
    
    newhtmlstring = newhtmlstring.replace("###datetime###",str(datetime.now()))
    newhtmlstring = newhtmlstring.replace("###temp###",str(data["temp"]))
    newhtmlstring = newhtmlstring.replace("###pressure###",str(data["pressure"]))
    newhtmlstring = newhtmlstring.replace("###humidity###",str(data["humidity"]))
    newhtmlstring = newhtmlstring.replace("###pmtwofive###",str(data["pmtwofive"]))
    newhtmlstring = newhtmlstring.replace("###pmten###",str(data["pmten"]))
    
    #print(newhtmlstring)
    homepage = open(path,'w')
    homepage.write(newhtmlstring)
    homepage.close()
    
htmlstring = "<html><head><title>Air Temp, Humidty, Pressure and Quality</title></head>\
<body><h1>Air Temp, Humidty, Pressure and Quality</h1>\
<table><tr><th>Date / Time</th><td>###datetime###</td></tr>\
<tr><th>Temp (f)</th><td>###temp###</td></tr>\
<tr><th>pressure</th><td>###pressure###</td></tr>\
<tr><th>humidity</th><td>###humidity###</td></tr>\
<tr><th>pmtwofive</th><td>###pmtwofive###</td></tr>\
<tr><th>pmten</th><td>###pmten###</td></tr>\
</table></body></html>"

def writetodb():
    '''
    This function is deprecated. Use writetoREST() instead.
    '''
    user="admin"
    password="xgKItSCvK6Fs5DtSov7w"
    endpoint="database-1.cluster-cx7osshnlikw.us-east-2.rds.amazonaws.com"
    #endpoint="172.31.0.0/20"    
    #database="database-1"#"environment_data"
    database="environment_data"
    
    # Open database connection
    db = pymysql.connect(endpoint,user,password,database)
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT * FROM observations")
    
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print ("one observation : %s " % data)
    
    # disconnect from server
    db.close()

'''
|----+----------+----------------------------------------------------------------------|
| id | name     | description                                                          |
|----+----------+----------------------------------------------------------------------|
|  1 | tempf    | Temperature (fahrenheit)                                             |
|  2 | tempc    | Temperature (celsius)                                                |
|  3 | humidity  | Humidity                                                             |
|  4 | pressure | Atmospheric Pressure                                                 |
|  5 | pm2.5    | Particulate matter (smaller than 2.5 microns) concentration in mg/m3 |
|  6 | pm10     | Particulate matter (smaller than 10 microns) concentration in mg/m3  |
|----+----------+----------------------------------------------------------------------|
'''
datatypemap = {
        'tempf':1,
        'tempc':2,
        'humidity':3,
        'pressure':4,
        'pmtwofive':5,
        'pmten':6
        }

def writetoREST():
    '''
    sample JSON payload:
    {
	"add_date": "2019-11-22T23:20:05.88Z",
	"obs_type": 6,
	"sensor": 1,
	"location": 1,
	"value": 1.2
    }
    '''
    data ={
        "add_date": "2019-11-24T23:20:05.88Z",
	"obs_type": 6,
	"sensor": 1,
	"location": 1,
	"value": 1.2
    }
    '''
    {'pressure': 1010.6982421875, 'temp': 92.24471817016601, 'humidity': 26.783153533935547, 'pmtwofive': 3.7, 'pmten': 5.6}
POST response:  <Response [201]>
    '''
    sensordata = getdata()
    data["add_date"] = str(datetime.now())
    # write temp
    data["obs_type"] = datatypemap["tempf"]
    data["value"] = sensordata["temp"]
    writePost(data)
    # write pressure
    data["obs_type"] = datatypemap["pressure"]
    data["value"] = sensordata["pressure"]
    writePost(data)
    # write humidity
    data["obs_type"] = datatypemap["humidity"]
    data["value"] = sensordata["humidity"]
    writePost(data)
    # write pmtwofive
    data["obs_type"] = datatypemap["pmtwofive"]
    data["value"] = sensordata["pmtwofive"]
    writePost(data)
    # write pmten
    data["obs_type"] = datatypemap["pmten"]
    data["value"] = sensordata["pmten"]
    writePost(data)


# The http headers that will be sent with each POST
headers = {'Content-Type': 'application/json'}
# The url for the REST service
endpointbase = 'http://node-express-env.quqvup2twn.us-east-2.elasticbeanstalk.com/'
# the url for the specific REST operation 
endpoint = endpointbase + 'add_observation'

def writePost(jsondata):
    '''
    writes the jsondata values to the REST service
    '''
    response = requests.post(endpoint, headers=headers, json=jsondata)
    print('POST response: ',response)    
    return response

if __name__ == '__main__':
    # note that each write*** function will make its own getdata() call
    # but I don't care.
    writehtml()
    writetoREST()
