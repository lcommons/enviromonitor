from PicoAirQuality import KitronikBME688
import machine
import utime
import Pico_16x2_LCD as LCD

LCD.setupLCD()
LCD.clearScreen()
LCD.displayString(1,0,'Starting up...')

bme688 = KitronikBME688()
LCD.displayString(1,0,'bme688 initialized...')
print("bme688 = KitronikBME688()")
bme688.setupGasSensor()
LCD.displayString(1,0,'calculating gas')
LCD.displayString(1,0,'sensor baseline')
print("bme688.setupGasSensor()")
bme688.calcBaselines()
LCD.displayString(1,0,'baselines complete')
print("bme688.calcBaselines()")


while(True):
    bme688.measureData()
    tempF = bme688.readTemperature("F")
    #tempC = bme688.readTemperature()
    #pressure = bme688.readPressure()
    humidity = bme688.readHumidity()

    LCD.displayString(1,0,'Temp: '+str(round(tempF,1))+'\337F')
    LCD.displayString(2,0,'Humidity: '+str(round(humidity,1))+'%')
    LCD.longDelay(5000)
    LCD.clearScreen()
    LCD.displayString(1,0,'IAQ: ' + str(bme688.getAirQualityScore()))
    LCD.displayString(2,0,'eCO2: '+ str(bme688.readeCO2()) + ' ppm')
    LCD.longDelay(5000)
    LCD.clearScreen()
    LCD.longDelay(100)
 