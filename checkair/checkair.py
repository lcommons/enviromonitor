#import pymysql
import serial
import json
import requests
from datetime import datetime
from sense_hat import SenseHat
import checktemp
import paho.mqtt.client as mqtt

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
or
*/1 * * * *  python3 /home/airpi12/temp2json.py
'''

datadict = {}
'''
# 2020-10-23 errors trying to initialize senseHat pressure and humidity;
# senseHat temp seems to work... but I don't need that.
# SOoooo... I'm eliminating Sense Hat for now.
def getsensehatdata():
    sense = SenseHat()
    sense.clear()
    #lhc 2020-10-23 pressure = sense.get_pressure()
    temp = sense.get_temperature()
    temp = 9.0/5.0 * temp + 32
    humidity = sense.get_humidity()
    #print("humidity: ", humidity)
    #print("temp : ", temp)
    #print("pressure: ", pressure)
    #lhc 2020-10-23 datadict["pressure"] = pressure
    datadict["temp"] = temp
    datadict["humidity"] = humidity
'''

def getppmdata():
    data = []
    ser = serial.Serial('/dev/ttyUSB0')
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)
        pmtwofive = int.from_bytes(
            b''.join(data[2:4]), byteorder='little') / 10
        pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    #print("pmtwofive: ", pmtwofive)
    #print("pmten: ", pmten)
    datadict["pmtwofive"] = pmtwofive
    datadict["pmten"] = pmten


def gettempdata(f=True):
    deg_c, deg_f = checktemp.read_temp()
    if (f):
        datadict["temp"] = deg_f
    else:
        datadict["temp"] = deg_c


def getdata():
    '''
    Remove call to senseHat
    sense = SenseHat()
    sense.clear()
    #lhc 2020-10-23 pressure = sense.get_pressure()
    temp = sense.get_temperature()
    temp = 9.0/5.0 * temp + 32
    humidity = sense.get_humidity()
    #print("humidity: ", humidity)
    #print("temp : ", temp)
    #print("pressure: ", pressure)
    '''
    data = []
    ser = serial.Serial('/dev/ttyUSB0')
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

        #print("data: ",data)
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

    #print("pmtwofive: ", pmtwofive)
    #print("pmten: ", pmten)

    datadic = {}
    #lhc 2020-10-23 datadic["pressure"] = pressure
    #lhc 2020-10-23 datadic["temp"] = temp
    #lhc 2020-10-23 datadic["humidity"] = humidity
    datadic["pmtwofive"] = pmtwofive
    datadic["pmten"] = pmten

    return datadic

def writehtml():
    path = "/var/www/html/index2.html"
    jsonPath = "/var/www/html/data2.json"

    #lhc 2020-10-23 getsensehatdata()
    getppmdata()
    gettempdata()
    datadict["timestamp"] = datetime.now().isoformat()
    with open(jsonPath, 'w') as fp:
        json.dump(datadict, fp)

    #print("getdata: ",data)
    newhtmlstring = htmlstring

    newhtmlstring = newhtmlstring.replace(
        "###datetime###", str(datadict["timestamp"]))
    newhtmlstring = newhtmlstring.replace("###temp###", str(datadict["temp"]))
    #lhc 2020-10-23 newhtmlstring = newhtmlstring.replace(
    #lhc 2020-10-23     "###temp2###", str(datadict["temp2"]))
    #lhc 2020-10-23 newhtmlstring = newhtmlstring.replace(
    #lhc 2020-10-23     "###pressure###", str(datadict["pressure"]))
#   newhtmlstring = newhtmlstring.replace("###pressure###", 'n/a')
    #lhc 2020-10-23 newhtmlstring = newhtmlstring.replace(
    #lhc 2020-10-23     "###humidity###", str(datadict["humidity"]))
#   newhtmlstring = newhtmlstring.replace("###humidity###",'n/a')
    newhtmlstring = newhtmlstring.replace(
        "###pmtwofive###", str(datadict["pmtwofive"]))
    newhtmlstring = newhtmlstring.replace(
        "###pmten###", str(datadict["pmten"]))

    # print(newhtmlstring)
    homepage = open(path, 'w')
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
    user = "admin"
    password = "xgKItSCvK6Fs5DtSov7w"
    endpoint = "database-1.cluster-cx7osshnlikw.us-east-2.rds.amazonaws.com"
    # endpoint="172.31.0.0/20"
    # database="database-1"#"environment_data"
    database = "environment_data"

    # Open database connection
    db = pymysql.connect(endpoint, user, password, database)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT * FROM observations")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    #print("one observation : %s " % data)

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
    'tempf': 1,
    'tempc': 2,
    'humidity': 3,
    'pressure': 4,
    'pmtwofive': 5,
    'pmten': 6
}
'''
#mosquitto_pub -h "$broker" -p 1883 -t "$topic" -m 
"{\"timestamp\":\"$timestamp\",\"hostname\":\"$HOSTNAME\",\"ip\":\"$ipaddr\",\"location\":12,\"type\":1,\"value\":$values}"
'''

# The callback function. It will be triggered when trying to connect to the MQTT broker
# client is the client instance connected this time
# userdata is users' information, usually empty. If it is needed, you can set it through user_data_set function.
# flags save the dictionary of broker response flag.
# rc is the response code.
# Generally, we only need to pay attention to whether the response code is 0.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        x=0
        #print("Connected success")
    else:
        x=1
        #print(f"Connected fail with code {rc}")
        
broker="192.168.0.110"
topic="observation/livingroom/temperature"
ip="192.168.0.176"
hostname="airpi"

client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker, 1883, 60)

def publishMqtt(jsondata):
    # "{\"timestamp\":\"$timestamp\",\"hostname\":\"{hostname}\",\"ip\":\"{ip}\",\"location\":12,\"type\":1,\"value\":$values}"
    message = "{\"timestamp\":\""\
        f"{jsondata['add_date']}"\
        "\",\"hostname\":\""\
        f"{hostname}"\
        "\",\"ip\":\""\
        f"{ip}"\
        "\",\"sensor\":\""\
        f"{jsondata['sensor']}"\
        "\",\"location\":"\
        f"{jsondata['location']}"\
        ",\"type\":"\
        f"{jsondata['obs_type']}"\
        ",\"value\":"\
        f"{jsondata['value']}"\
        "}"

    #print(message)
    client.publish(topic, payload=message, qos=0, retain=False)

def writetoMqtt():
    data = {
        "add_date": '',  # "2019-11-24T23:20:05.88Z",
        "obs_type": 6,
        "sensor": "",
        "location": 1,
        "value": 0  # 1.2
        # http://app.commons-faith.es/observations/
    }

    getppmdata()
    gettempdata()

    # write temp from external temp sensor
    data["add_date"] = str(datetime.now().isoformat())
    data["sensor"] = "28-01144c5d43aa"  # the external temp sensor
    data["obs_type"] = datatypemap["tempf"]
    data["value"] = datadict['temp']  # gettemp()#sensordata["temp"]
    publishMqtt(data)
    
    # write pmtwofive
    data["sensor"] = ""
    data["obs_type"] = datatypemap["pmtwofive"]
    data["value"] = datadict["pmtwofive"]
    publishMqtt(data)
    
    # write pmten
    data["sensor"] = ""
    data["obs_type"] = datatypemap["pmten"]
    data["value"] = datadict["pmten"]
    publishMqtt(data)
    
def writetoREST():
    data = {
        "add_date": '',  # "2019-11-24T23:20:05.88Z",
        "obs_type": 6,
        "sensor": 1,
        "location": 1,
        "value": 0  # 1.2
        # http://app.commons-faith.es/observations/
    }
    '''
    {'pressure': 1010.6982421875, 'temp': 92.24471817016601, 'humidity': 26.783153533935547, 'pmtwofive': 3.7, 'pmten': 5.6}
POST response:  <Response [201]>
    '''
    #sensordata = getdata()
    #lhc 2020-10-23 getsensehatdata()
    getppmdata()
    gettempdata()

    # write temp from external temp sensor
    data["add_date"] = str(datetime.now())
    data["sensor"] = 2  # the external temp sensor
    data["obs_type"] = datatypemap["tempf"]
    data["value"] = datadict['temp']  # gettemp()#sensordata["temp"]
    writePost(data)

    # write temp from sensehat
    data["sensor"] = 1
    data["obs_type"] = datatypemap["tempf"]
    data["value"] = datadict['temp']  # gettemp()#sensordata["temp"]
    writePost(data)

    # write pressure
    #lhc 2020-10-23 data["obs_type"] = datatypemap["pressure"]
    #lhc 2020-10-23 data["value"] = datadict["pressure"]
    writePost(data)
    # write humidity
    #lhc 2020-10-23 data["obs_type"] = datatypemap["humidity"]
    #lhc 2020-10-23 data["value"] = datadict["humidity"]
    #lhc 2020-10-23 writePost(data)

    # write pmtwofive
    data["obs_type"] = datatypemap["pmtwofive"]
    data["value"] = datadict["pmtwofive"]
    writePost(data)
    # write pmten
    data["obs_type"] = datatypemap["pmten"]
    data["value"] = datadict["pmten"]
    writePost(data)


# The http headers that will be sent with each POST
headers = {'Content-Type': 'application/json',
           'Authorization': 'aljkhds(92@34lkj-sdf897;128H:HUW<HEHk'}
# The url for the REST service
#endpointbase = 'http://node-express-env.quqvup2twn.us-east-2.elasticbeanstalk.com/'
endpointbase = 'https://app.commons-faith.es/'
# the url for the specific REST operation
endpoint = endpointbase + 'add_observation'


def writePost(jsondata):
    '''
    writes the jsondata values to the REST service
    '''
    response = requests.post(endpoint, headers=headers, json=jsondata)
    #print('POST response: ', response)
    return response


def gettemp(f=True):
    deg_c, deg_f = checktemp.read_temp()
    if (f):
        return deg_f
        #print(" ffffff: ",deg_f)
    else:
        return deg_c
        #print("cccccc: ",deg_c)


if __name__ == '__main__':
    # note that each write*** function will make its own getdata() call
    # but I don't care.
    writehtml()
    # writetoREST()
    writetoMqtt()
    # gettemp()
    # print(checktemp.read_temp())
