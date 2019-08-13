# Kindle weather page

![weatherPageExampl](weatherPageExample.jpg)

## This project consists of two distinct parts:
1) a python script which retrieves weather report and forecast pages from the National Weather Service, parses those pages to extract specific content, and builds an HTML page with the desired content.
2) A NodeJS web server which hosts a REST service to serve the HTML page.

A CRON job can generate a new web page every hour, several minutes after the page is normally updated.

The Node REST service can also refresh the web page on demand.

# Setup
1) Clone the project to your local system.
2) Run npm install to download the  dependencies for the Node server.
3) type ```$ node kindleserver.js``` to start the server.
4) in your browser, load localhost and a sample weather page should display.

## The cron job
The current conditions data is update at xx:51, but the new page isn’t available until 5-10 minutes after the hour.
```
pi@naspberry ~/kindleServer $ crontab -l
# m h  dom mon dow   command

15 * * * * python3 /home/pi/kindleServer/getWeather.py
pi@naspberry ~/kindleServer $
```
