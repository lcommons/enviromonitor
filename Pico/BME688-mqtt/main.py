import network
import socket
import time
from PicoAirQuality import KitronikBME688

from machine import RTC
import uasyncio as asyncio
from umqtt.simple import MQTTClient
import uasyncio

rtc=RTC()

tempTopic = 'observation/pico/temperature/'
humidityTopic = 'observation/pico/humidity/'
client_id='pico'
mqtt_server='192.168.1.201'
hostname="airpiPico"
ip="192.168.1.79"
sensor='bme688'
location=199
type=1

#led = Pin(15, Pin.OUT)
#onboard = Pin("LED", Pin.OUT, value=0)

#ssid = 'A Network'
#password = 'A Password'

bme688 = KitronikBME688()
print("bme688 = KitronikBME688()")
bme688.setupGasSensor()
print("bme688.setupGasSensor()")
bme688.calcBaselines()
print("bme688.calcBaselines()")

wlan = network.WLAN(network.STA_IF)
def connect_to_network():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Disable power-save mode
    #wlan.connect(ssid, password)
    wlan.connect("wifibecausefi","spicyhotsalsa")

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for WIFI connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

def mqtt_connect():
    print("...mqtt_connect...")
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client
    
def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   time.sleep(5)
   machine.reset()
   
async def main():
    print('Connecting to Network...')
    connect_to_network()
    try:
        print("about to connect to NS1")
        client = mqtt_connect()
    except OSError as e:
        print("error about to reconnect NS1")
        #reconnect()
        client = mqtt_connect()
        
    while True:
        bme688.measureData()
        tempF = bme688.readTemperature("F")
        humidity = bme688.readHumidity()
        timestamp=rtc.datetime()
        timestring="%04d-%02d-%02dT%02d:%02d:%02d"%(timestamp[0:3] +
                                                    timestamp[4:7])
        '''
        {
          "timestamp": "2023-10-14T14:13:03.621-0400",
          "hostname": "airpi13",
          "ip": "192.168.1.213 ",
          "sensor": "28-01144aac98aa",
          "location": 101,
          "type": 1,
          "value": 61.925
        }

        tempTopic = 'observation/pico/temperature/'
        humidityTopic = 'observation/pico/humidity/'

        '''
        tempString = '{"timestamp": "'+timestring + '","hostname":"'+hostname+'","ip": "'+ip+'","sensor": "pico-test","location": 999,"type": 1,"value":'+str(round(tempF,1))+'}'
        print(tempString)
        client.publish(tempTopic, tempString)
        humidString = '{"timestamp": "'+timestring + '","hostname":"'+hostname+'","ip": "'+ip+'","sensor": "pico-test","location": 999,"type": 3,"value":'+str(round(humidity,1))+'}'
        #"+'"temp": '+str(round(tempF,1))+','+' "humidity": '+str(round(humidity,1))+'}\r\n'
        print(humidString)
        client.publish(humidityTopic, humidString)
        print("published")
        await uasyncio.sleep(60)
        
    
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()