#!/usr/bin/env python

# still to do:
# - DONE use night icons at night; add "day - " or "night - " to the text
# - error handling if xml isn't available
# - error handling if weather conditions aren't found
# - add more icons to the list
#
import requests
import xml.etree.ElementTree as ET
from datetime import datetime


currentWeatherURL = 'http://w1.weather.gov/xml/current_obs/KPVD.xml'
currentWeatherResponse = requests.get(currentWeatherURL)
zipcode='02863'

forecastURL = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php?whichClient=NDFDgenByDayMultiZipCode&zipCodeList='+zipcode+'&format=12+hourly&numDays=2&Unit=e'

imgnamesday = {
'Fog':'20',
'fog':'20',
'Patchy Fog':'20',
'Fog/Mist':'20',
'A Few Clouds':'34',
'A Few Clouds and Breezy':'23',
'Cloudy':'26',
'Increasing Clouds':'28',
'Mostly Cloudy':'28',
'Mostly Cloudy and Breezy':'23',
'Mostly Cloudy and Windy':'24',
'Overcast and Breezy':'26',
'Chance Drizzle':'9',
'Rain':'11',
'Light Rain':'11',
'light rain':'11',
'light rain showers':'11',
'light freezing rain':'5',
'moderate rain showers':'11',
'moderate rain':'11',
'Light Rain Fog/Mist':'11',
'Rain Fog/Mist':'11',
'Rain Fog/Mist and Breezy':'1',
'Heavy Rain Fog/Mist':'12',
'heavy rain showers':'12',
'Heavy Rain Fog/Mist and Breezy':'1',
'Rain Likely':'11',
'none thunderstorms':'35',
'Overcast':'26',
'Overcast':'26',
'Overcast and Windy':'24',
'Fair':'32',
'Fair and Breezy':'32',
'Clear':'32',
'Cold':'32',
'Becoming Clear':'32',
'Becoming Sunny':'32',
'Sunny':'32',
'Mostly Clear':'32',
'snow':'13',
'heavy snow':'15',
'light snow':'13',
'snow showers':'13',
'light snow showers':'13',
'Light Snow':'13',
'Light Snow Freezing Fog':'13',
'Light Snow and Breezy':'43',
'Light Snow Fog/Mist':'13',
'Light Snow Fog/Mist and Breezy':'43',
'Light Snow Blowing Snow and Breezy':'43',
'Snow Freezing Fog and Breezy':'43',
'Snow Freezing Fog':'42',
'Snow Likely':'14',
'Chance Snow':'14',
'moderate snow':'41',
'Mostly Sunny':'34',
'Partly Sunny':'44',
'Partly Cloudy':'30',
'Decreasing Clouds':'44',
'Chance Rain Showers':'9'
}

imgnamesnight = {
'Fog':'20',
'fog':'20',
'Patchy Fog':'20',
'Fog/Mist':'20',
'A Few Clouds':'29_2',
'A Few Clouds and Breezy':'23',
'Cloudy':'26',
'Increasing Clouds':'28',
'Mostly Cloudy':'27',
'Mostly Cloudy and Breezy':'23',
'Chance Drizzle':'9',
'Rain':'11',
'Light Rain':'11',
'light rain':'11',
'light rain showers':'11',
'light freezing rain':'5',
'moderate rain showers':'11',
'moderate rain':'11',
'Light Rain Fog/Mist':'11',
'Rain Fog/Mist':'11',
'Rain Fog/Mist and Breezy':'1',
'Heavy Rain Fog/Mist':'12',
'heavy rain showers':'12',
'Heavy Rain Fog/Mist and Breezy':'1',
'Rain Likely':'11',
'none thunderstorms':'35',
'overcast':'26',
'Overcast':'26',
'Overcast and Windy':'24',
'Fair':'31_2',
'Fair and Breezy':'31_2',
'Clear':'31_2',
'Mostly Clear':'31_2',
'Becoming Clear':'31_2',
'Overcast and Breezy':'26',
'Light Snow':'13',
'Light Snow Freezing Fog':'13',
'Light Snow and Breezy':'43',
'Light Snow Fog/Mist':'13',
'Light Snow Fog/Mist and Breezy':'43',
'Light Snow Blowing Snow and Breezy':'43',
'Snow Freezing Fog and Breezy':'43',
'Snow Freezing Fog':'42',
'snow':'13',
'heavy snow':'15',
'light snow':'13',
'snow showers':'13',
'light snow showers':'13',
'Snow Likely':'14',
'Chance Snow':'14',
'moderate snow':'41',
'Mostly Sunny':'33',
'Partly Sunny':'44',
'Partly Cloudy':'29',
'Mostly Cloudy and Windy':'24',
'Decreasing Clouds':'44',
'Chance Rain Showers':'9'
}


forecastResponse = requests.get(forecastURL)
root = ET.fromstring(forecastResponse.content)

pathToImages = 'Flat Black/'; 

period = []
period.append({})
period.append({})
period.append({})
period.append({})

isEvening = False;

PeriodNames = root.findall(".//*[layout-key='k-p12h-n4-3']//*[@period-name]")

if  PeriodNames[0].get('period-name').find('ight') >=0:
    isEvening = True;

#print( PeriodNames[0].get('period-name'))
#print( PeriodNames[0].get('period-name').find('ight'))
#print( PeriodNames[1].get('period-name').find('ight'))
#print( 'isEvening: ' )
#print( isEvening )

print(PeriodNames[0].get('period-name'))
print(PeriodNames[1].get('period-name'))
print(PeriodNames[2].get('period-name'))
print(PeriodNames[3].get('period-name'))

#DayNames = root.findall(".//*[layout-key='k-p24h-n2-1']//*[@period-name]")
#NightNames = root.findall(".//*[layout-key='k-p24h-n2-2']//*[@period-name]")
#maxTemps = root.findall(".//*[type='maximum']/value")
maxTemps = root.findall(".//temperature[@type='maximum']/value")
minTemps = root.findall(".//temperature[@type='minimum']/value")
conditions = root.findall(".//*weather-conditions")

#print(DayNames[0].text)
#print(NightNames[0].text)
print(maxTemps[0].text)
print(minTemps[0].text)
print(conditions[0].text)

imgText1 = "<img src='"
imgText2 = "'/>"

if isEvening:
    period[1]['temp'] = maxTemps[0].text
    period[0]['temp'] = minTemps[0].text
    period[3]['temp'] = maxTemps[1].text
    period[2]['temp'] = minTemps[1].text
    evenImages = imgnamesday
    oddImages = imgnamesnight
else:
    period[0]['temp'] = maxTemps[0].text
    period[1]['temp'] = minTemps[0].text
    period[2]['temp'] = maxTemps[1].text
    period[3]['temp'] = minTemps[1].text
    evenImages =  imgnamesnight
    oddImages = imgnamesday

for i in range(4):
    print(i)
    print(PeriodNames[i].get('period-name'))
    period[i]['name']  = PeriodNames[i].get('period-name')

#    if conditions[i] == None:
#        print('conditions[i] == None')
#        period[i]['weather'] = ''
#        period[i]['chance'] = ''
#    el
    if conditions[i].find('value') == None OR 'Fog' in conditions[i].find('value'):
        print(conditions[i].get('weather-summary'))
        if conditions[i].get('weather-summary') == None:
            period[i]['weather'] = '' #TODO add default weather icon (sunny/clear) if no forecast is provided
        else: 
            period[i]['weather'] = conditions[i].get('weather-summary')
        period[i]['chance'] = ''
    else:
        print(conditions[i].find('value').get('coverage'))
        print(conditions[i].find('value').get('intensity'))
        print(conditions[i].find('value').get('weather-type'))
        period[i]['weather'] = conditions[i].find('value').get('intensity') + ' ' + conditions[i].find('value').get('weather-type')
        period[i]['chance'] = conditions[i].find('value').get('coverage')
 
imgText1 = "<img src='"
imgText2 = "'/>"

if period[0]['weather'] in oddImages:
    period[0]['icon'] = imgText1 + pathToImages + oddImages[period[0]['weather']] + '.png' + imgText2
else:
    period[0]['icon'] = period[0]['weather']

if period[1]['weather'] in evenImages:
    period[1]['icon'] = imgText1 + pathToImages + evenImages[period[1]['weather']] + '.png' + imgText2 
else:
    period[1]['icon'] = period[1]['weather']

if period[2]['weather'] in oddImages:
    period[2]['icon'] = imgText1 + pathToImages + oddImages[period[2]['weather']] + '.png' + imgText2
else:
    period[2]['icon'] = period[2]['weather']

if period[3]['weather'] in evenImages:
    period[3]['icon'] = imgText1 + pathToImages + evenImages[period[3]['weather']] + '.png' + imgText2
else:
    period[3]['icon'] = period[3]['weather']

root = ET.fromstring(currentWeatherResponse.content)

currentTemp = root.findall("temp_f")[0].text
currentWeather = root.findall("weather")[0].text

currentWindchillNode = root.find("windchill_f")
if currentWindchillNode is None:
    #currentWindchill = ''
    currentWindchill = currentTemp
else:
    currentWindchill = root.findall("windchill_f")[0].text

currentTime = root.findall("observation_time")[0].text

currentTime = currentTime.replace('Last Updated on ','')
currentTime = currentTime.replace('EST','')

if currentWeather in  oddImages:
    currentIcon = imgText1 + pathToImages +  oddImages[currentWeather] + '.png' + imgText2
else:
    currentIcon = currentWeather

#f = open('/home/pi/kindleServer/output.html','w')
f = open('output.html','w')
f.write("<html><head><title>Weather Forecast</title><link rel='stylesheet' type='text/css' href='kindle.css'><script type='text/javascript'>setInterval(function() {window.location.reload();}, 60*60000); //NOTE: period is passed in milliseconds</script><head><body>")
f.write("<div id='current'><span id='current-temp' class='current-temp'>"+currentTemp+"&deg;<br/><span id='windchill'>("+currentWindchill+"&deg;)</span></span><span id='current-img'>" + currentIcon + "</span></div>")
f.write("<div id='day1'><span class='period1' title='hello world'><div class='label'>"+period[0]['name']+ "</div>"+ period[0]['icon']+period[0]['chance'] +"<div class='temp'>"+period[0]['temp']+"&deg;</div></span>")
f.write("<span class='period2'><div class='label'>"+period[1]['name']+ "</div>"+ period[1]['icon']+period[1]['chance'] +"<div class='temp'>"+ period[1]['temp']+"&deg;</div></span></div>")
f.write("<div id='day2'><span class='period1'><div class='label'>"+period[2]['name']+ "</div>"+ period[2]['icon'] +period[2]['chance'] +"<div class='temp'>"+period[2]['temp']+"&deg;</div></span>")
f.write("<span class='period2'><div class='label'>"+period[3]['name']+ "</div>"+ period[3]['icon'] +period[3]['chance'] +"<div class='temp'>"+ period[3]['temp']+"&deg;</div></span></div>")
f.write("<div class='footer'>Data: "+currentTime+ "; Page " + datetime.now().strftime('%b %d %Y, %H:%M %p') + "</div>")
f.write("<div class='footer'><pre>;debugOn (press enter)<br/>~disableScreensaver (press enter)<br/>;debugOff (press enter)</pre></div>")
f.write("</body></html>")
f.close()
#print(then.astimezone(pytz.timezone('US/Eastern')))
