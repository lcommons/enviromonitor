# Kindle weather page

![weatherPageExampl](weatherPageExample.jpg)

## This project consists of three distinct sub-projects:
1) The Tablet Weather page, shown above. This is a standalone project.
2) A python script with reads air-quality information on a Raspberry Pi and
  - updates a static web page served by a webserver running on that pi;
  - writes the data to a cloud-based REST servive for storage (see the next item)
3) A REST service based on Express and node.js which provides an interface to a database that stores the air quality data.

