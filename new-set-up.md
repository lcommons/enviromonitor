# setting up a Raspberry Pi as an environment monitor

## Temperature sensor on a Raspberry Pi Zero

### use existing Python3 script to read temp and write index.html and json

### use the new html page created for the JS app.

### run lighttpd

- Serve on port 80
- path = "/var/www/html/index.html" <--
- jsonPath = "/var/www/html/data.json"

### in real time

2020-09-11 11:14
on airpi12
$ sudo apt-get install lighttpd
$ sudo chown airpi12 /var/www/html
\$ nano /var/www/html/index.html
created a placeholder page

2020-09-11 20:42

Create cron job to run the script every minute

`*/1 * * * * python3 /path/to/checkair.py`

or

`*/1 * * * * python3 /home/airpi12/temp2json.py`

2020-09-12

- created new python script, temp2json.py, that gets the temp and writes data.json.
  I copied this from checkair.py and removed the crud.
- updated crontab to run this new file.
- I deleted all the other enviromonitor stuff.
- Copied webpage and css to /var/www/html
