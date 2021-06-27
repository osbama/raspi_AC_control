#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

########################################################################
# Osman Baris Malcioglu. GPL 
# This script detects power losses (via UPS) and temperature (via MPL115A2)
# and sends a pre recorded IR blast when certain criteria are met. 
########################################################################

import os
import subprocess
import sys
import LCD.I2C_LCD_driver as I2C_LCD_driver
from PSU.UPSLite import UPSLite
import ENV.I2C_MPL115A2_driver as I2C_MPL115A2_driver
from time import *
import netifaces as ni
import RPi.GPIO as GPIO
import asyncio
import logging


## Maximum Temperature
max_temp=26.0
## Wait time before sending AC on
wait_ac=30
## AC ON command with desired environment settings
AC_ON_COMMAND="Vestel-on.txt"
## Number of times AC_ON_COMMAND is sent
AC_RETRY=3

#initialize LCD, UPS, MPL115A2
mylcd = I2C_LCD_driver.lcd()
myups = UPSLite()
mysens = I2C_MPL115A2_driver.MPL115A2()
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
#print(ni.interfaces())
myups.PowerOnReset()
myups.QuickStart()

def turn_on_ac(reason):
    #IR remotes are different from TV remotes, they send everything at once.
    #In my case (VESTEL AC) the max timeout in kernel is more than enough to 
    #capture data, just use ir-ctl -d /dev/lirc1 -r -t 1250000 >Vestel-on.txt
    #and edit the file to remove the last 'timeout' line 
    #This routine will playback the captured file
    mylcd.lcd_clear()
    mylcd.lcd_display_string(reason,1)
    mylcd.lcd_display_string("AC/on in ",2)
   
    for i in range (0, wait_ac):
        mylcd.lcd_display_string("%02d"%(wait_ac-i),2,12)
        sleep(1)
    try:
        for j in range(0,AC_RETRY):
            #result = subprocess.run(["ir-ctl", "-d","/dev/lirc0","-S", necCommand], capture_output=True, check=True)
            result = subprocess.run(['ir-ctl -d /dev/lirc0 --send='+AC_ON_COMMAND], shell=True, capture_output=True, check=True)
            print(result)
            sleep(1)
    except:
        logging.error("ir-ctl subprocess failed")
        return

    logging.info("AC/ON sent")
    

def main (argv):
    logging.basicConfig(format='%(asctime)s %(message)s')
    #Spacing between scrolling text
    str_pad = " " * 1
    #initial Power status
    if (GPIO.input(4) == GPIO.HIGH):
        powered = True
    else:
        powered = False
    #Prepare screen
    mylcd.lcd_clear()
    power_loss_count=0
    mylcd.backlight(0)
    
    while True:
        #Slow update
        ifaces=["eth0","wlan0"]
        iface_string = ""
        for iface in ifaces:
            try:
                iface_string = iface_string+iface+":"+ni.ifaddresses(iface)[2][0]['addr']+" "
            except:
                iface_string = iface_string+iface+":"+"N/A "

        iface_string = str_pad + iface_string
        temperature,pressure=mysens.read_data()
        info_string="B:%2i%%" % myups.readCapacity()+" PL:%3i" % power_loss_count+" T:%3.2f C"%temperature+" P:%3.2f KPa"%pressure+" "
        info_string = str_pad + info_string

        if len(iface_string) > len(info_string) :
            info_string=info_string+" "*(len(iface_string)-len(info_string))
            length=len(iface_string)
        else:
            iface_string=iface_string+" "*(len(info_string)-len(iface_string))
            length=len(info_string)

        if (temperature > max_temp) :
            turn_on_ac(reason="Temperature")

        #Fast update
        for i in range (0, length):
            lcd_text1 = iface_string[i:(i+16)]
            mylcd.lcd_display_string(lcd_text1,1)
            lcd_text2 = info_string[i:(i+16)]
            mylcd.lcd_display_string(lcd_text2,2)

            sleep(0.4)
            if (GPIO.input(4) == GPIO.HIGH) and not powered :
                powered=True
                logging.warning("Power restored")
                turn_on_ac(reason="Power")
            if (GPIO.input(4) == GPIO.LOW) and powered:
                powered=False
                logging.warning("Power lost")
                power_loss_count+=1
 
            mylcd.lcd_display_string(str_pad,1)
            mylcd.lcd_display_string(str_pad,2)

if __name__ == "__main__":
    main(sys.argv[1:])
