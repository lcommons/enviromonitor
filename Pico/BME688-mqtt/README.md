# MQTT on a PICO
This POC publishes BME688 readings to MQTT using a local MQTT Broker.

STATUS 2023-10-28
This runs OK when connected to Thonny. Well, not really OPK. It takes numerous restarts before it works.
Without Thonny, it doesn't run... but maybe if I was more persistent and tried a few (dozen) more times it would work?

TO DO
 - blink the LED at each startup milestone to provide minimal feedback on startup status
 - only use Pico with LCD since cant SSH or check status in any other way?
 - IN A NEW PROJECT combine http service of heartbeat/status, JSON, web page
 - in another new project, combine LCD, SD data persistance, HTTP, and MQTT
    - this is seperate from the un-networked BME688/LCD/SD-card project.