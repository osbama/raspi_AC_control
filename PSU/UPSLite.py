__author__ = 'obm'
import struct
import smbus
import sys

class UPSLite:
    """
    This class is designed for accessing UPS Lite for Pi Zero by ACE design
    """
    def __init__(self,address=0x36):
        """
        Initialize the communications with the UPS_Lite. Notice that SPI and I2C must be enabled
        see https://github.com/linshuqin329/UPS-Lite/blob/master/UPS_Lite.py
        i2cdetect -l
        i2cdetect -y 1
        :param address: Default address is 0x36
        """
        self.bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self.address=address

    def readVoltage(self):
        """This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"""
        read = self.bus.read_word_data(self.address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage

    def readCapacity(self):
        """This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"""
        read = self.bus.read_word_data(self.address, 4)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity
    def QuickStart(self):
        self.bus.write_word_data(self.address, 0x06,0x4000)
    def PowerOnReset(self):
        self.bus.write_word_data(self.address, 0xfe,0x0054)
