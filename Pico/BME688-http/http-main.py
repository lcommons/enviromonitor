import socket
import network
from PicoAirQuality import KitronikBME688

bme688 = KitronikBME688()
print("bme688 = KitronikBME688()")
bme688.setupGasSensor()
print("bme688.setupGasSensor()")
bme688.calcBaselines()
print("bme688.calcBaselines()")

page = open("index.html", "r")
html = page.read()
page.close()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("wifibecausefi","spicyhotsalsa")
sta_if = network.WLAN(network.STA_IF)
print(sta_if.ifconfig()[0])
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

while True:
    isdata = False
    cl, addr = s.accept()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        isdata = isdata or 'GET /data.json' in line
        if 'GET' in line:
            print(line)
        if not line or line == b'\r\n':
            break
    if isdata:
        bme688.measureData()
        tempF = bme688.readTemperature("F")
        #tempC = bme688.readTemperature()
        #pressure = bme688.readPressure()
        humidity = bme688.readHumidity()
        response = '{"timestamp": na,'+'"temp": '+str(round(tempF,1))+','+' "humidity": '+str(round(humidity,1))+'}\r\n'
    else:
        response = html 

    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
