.. highlight:: bash

I2C in Raspbian
==============================

`UPS Lite <https://hackaday.io/project/173847-ups-lite>`_ ; `Adafruit MPL115A2 Temp/Pressure sensor <https://www.adafruit.com/product/992>`_ and `2x16 I2C LCD <https://funduino.de/nr-19-i%C2%B2c-display>`_ use I2C protocol to communicate with the Raspberry Pi. 

Enabling I2C
---------------

First, log in to your Pi and enter ``sudo raspi-config`` to access the configuration menu. Then arrow down and select “Advanced Settings”. Arrow down and select “I2C Enable/Disable automatic loading” Choose “Yes” at the next prompt, exit the configuration menu, and reboot the Pi to activate the settings. 

Scanning the I2C addresses
---------------------------------

`I2C-tools`, is a program for scanning the I2C address of the connected peripherals. Install it with ``sudo apt-get install i2c-tools``.

With peripherals connected and I2C bus working use ``i2cdetect -y 1`` to scan the I2C bus and the adresses of the peripherals. These are usually preset from factory, and you don't have control over them. 

Interfacing with I2C peripherals from Python
-------------------------------------------------

`SMBUS`, contains the Python library for accessing the I2C bus on the Pi. At the command prompt, enter ``sudo apt-get install python3-smbus``.





