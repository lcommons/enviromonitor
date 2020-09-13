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

`*/1 * * * * python3 /home/airpi11/temp2json.py`

2020-09-12

- created new python script, temp2json.py, that gets the temp and writes data.json.
  I copied this from checkair.py and removed the crud.
- updated crontab to run this new file.
- I deleted all the other enviromonitor stuff.
- Copied webpage and css to /var/www/html

2020-09-13

- updated airpi12 index.html to include room label
- updated temp2json to read onewire sensore directly, not import another file.
- copy from airpi12 to chromebook
  $ scp airpi12@192.168.0.162:/home/airpi12/temp2json.py .
   $ scp airpi12@192.168.0.162:/var/www/html/\* .
- copy /var/www/html/\* to airpi11
- copy temp2json.py to airpi11
- further edits and updates to index.html and temp2json.py
- edit crontab on airpi11:
  - crontab -e
  - `*/1 * * * * python3 /home/airpi11/temp2json.py`
- copy updated index.html from airpi11 to airpi12
- AIRPI
  - disable old cron job
  - copy temp2json.py
  - copy /var/www/html/\*
  - update title and header of index.html
  - crontab -e
  - `*/1 * * * * python3 /home/airpi/temp2json.py`
