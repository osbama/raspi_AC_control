#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
O. Baris Malcioglu
Made available under GNU GENERAL PUBLIC LICENSE

# Modified from 
# https://www.raspberrypi.org/forums/viewtopic.php?t=91185

"""
# i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
I2CBUS = 1

# Sensor Address
ADDRESS = 0x60

import smbus
from time import sleep

class i2c_device:
   def __init__(self, addr, port=I2CBUS):
      self.addr = addr
      self.bus = smbus.SMBus(port)

# Write a single command
   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)

# Write a command and argument
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      sleep(0.0001)

# Write a block of data
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      sleep(0.0001)

# Read a single byte
   def read(self):
      return self.bus.read_byte(self.addr)

# Read
   def read_data(self, cmd):
      return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
   def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)

class MPL115A2:
   #initializes objects and lcd
   def __init__(self):
      self.sensor = i2c_device(ADDRESS)
      # a0: 16 bits - 1 sign, 12 int, 3 frac
      a0=(self.sensor.read_data(0x04)<<8) | \
               self.sensor.read_data(0x05)
      if a0 & 0x8000:
          a0d = -((~a0 & 0xffff) + 1)
      else:
          a0d = a0
      self.a0f = float(a0d) / 8.0
      #print("a0 = 0x%4x %5d %4.3f" % (a0, a0d, self.a0f))
      # b1: 16 bits - 1 sign, 2 int, 13 frac
      b1 = (self.sensor.read_data(0x06) << 8 ) | \
          self.sensor.read_data(0x07)
      if b1 & 0x8000:
          b1d = -((~b1 & 0xffff) + 1)
      else:
          b1d = b1
      self.b1f = float(b1d) / 8192.0
      #print("b1 = 0x%4x %5d %1.5f" % (b1, b1d, self.b1f))
      # b2: 16 bits - 1 sign, 1 int, 14 frac
      b2 = (self.sensor.read_data(0x08) << 8) | \
                 self.sensor.read_data(0x09)
      if b2 & 0x8000:
          b2d = -((~b2 & 0xffff) + 1)
      else:
          b2d = b2
      self.b2f = float(b2d) / 16384.0
      #print("b2 = 0x%4x %5d %1.5f" % (b2, b2d, self.b2f))
      # c12: 14 bits - 1 sign, 0 int, 13 frac
      # (Documentation in the datasheet is poor on this.)
      c12 = (self.sensor.read_data(0x0a) << 8) | \
                  self.sensor.read_data(0x0b)
      if c12 & 0x8000:
          c12d = -((~c12 & 0xffff) + 1)
      else:
          c12d = c12
      self.c12f = float(c12d) / 16777216.0
      #print("c12 = 0x%4x %5d %1.5f" % (c12, c12d, self.c12f))

   def read_data(self):
       # Start conversion and wait 3mS
       self.sensor.write_cmd_arg(0x12, 0x0)
       sleep(0.003)
       rawpres = (self.sensor.read_data(0x00) << 2) | \
                 (self.sensor.read_data(0x01) >> 6)
       rawtemp = (self.sensor.read_data(0x02) << 2) | \
                 (self.sensor.read_data(0x03) >> 6)
       #print("\nRaw pres = 0x%3x %4d" % (rawpres, rawpres))
       #print("Raw temp = 0x%3x %4d" % (rawtemp, rawtemp))
       pcomp = self.a0f + (self.b1f + self.c12f * rawtemp) * rawpres + self.b2f * rawtemp
       pkpa = pcomp / 15.737 + 50
       #print("Pres = %3.2f kPa" % pkpa)
       temp = 25.0 - (rawtemp - 498.0) / 5.35
       #print("Temp = %3.2f" % temp)
       return temp,pkpa
