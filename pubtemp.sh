#!/bin/bash
##########################
# 1) Call checktemp.py to get the current temperature
#
# 2) publish the temp value with the mosquitto client
#broker=192.168.1.110
broker=ns1.net.airpi.us
topic="observation/livingroom/temperature"
values=`python3 checktemp.py`
ipaddr=`hostname -I`
timestamp=$(date +"%Y-%m-%dT%T.%3N%z")
#echo "timestamp:$timestamp, hostname:$HOSTNAME, ip:$ipaddr, temp:$values"
#mosquitto_pub -h "$broker" -p 1883 -t "$topic" -m "{\"timestamp\":\"$timestamp\",\"hostname\":\"$HOSTNAME\",\"ip\":\"$ipaddr\",\"temp\":$values}"
mosquitto_pub -h "$broker" -p 1883 -t "$topic" -m "{\"timestamp\":\"$timestamp\",\"hostname\":\"$HOSTNAME\",\"ip\":\"$ipaddr\",\"location\":1,\"type\":1,\"value\":$values}"
