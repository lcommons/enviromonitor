import pymysql
import serial
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
    
if __name__ == '__main__':
    #writehtml()
    writetodb()
