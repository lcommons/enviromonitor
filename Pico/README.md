# Projects for the Raspberry Pi Pico/W

The Raspberry Pi Pi, and its WIFI-enabled cousin, the PicoW (aka Pi Cow), is a very small, low resource, low energy micro-computer. Unlike other Pis, it doesn't even have a recognizable operating system. It is really a new, unrelated machine.

I am experimenting with using the Pico/W for remote senor use: monitoring temperature and humidity in a solar kiln with no power, so I have to rely on small solar panels and small batteries to run the pico. If this works out, the Pico/W could be useful in lots of places where I just need to support a temp or other sensor and collect/publish data. Its cheaper, smaller, and lower-power than the Pi Zero.

But the PiZero runs a real OS. I can SSH into a Zero to monitor and hack the code. It runs a reall full version of Python. The Pico has a much less flexible development model.

## Project Ideas
- Solar Kiln monitor
   - BME688 monitor
   - LCD Display of current observations (and other data?)
   - data written to SD card for external use

- SAME AS ABOVE, plus
   - WIFI: HTTP and MQTT publishing

- Temp/Humidity/IAQ monitor
  - BME688 sensot
  - HTTP/MQTT publishing
  - optional LCD display

- OneWire sensors
  - use 1-Wire sensors for temp monitoring of Hot Tub or HVAC control