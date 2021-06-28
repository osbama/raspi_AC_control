.. highlight:: python


Adafruit MPL115A2 Temp/Pressure sensor
==========================================

This project uses a `Adafruit MPL115A2 Temp/Pressure sensor <https://www.adafruit.com/product/992>`_ . This sensor is intended for Arduino, and Adafruit does not share a method for interfacing with it using Raspberry Pi. Luckily I found someone that did the heavy lifting, and adapted the `ENV/I2C_MPL115A2_driver.py` from his code. The original post is below. 




Original post for interfacing with the MPL115A2 sensor in Python
---------------------------------------------------------------------


The following is duplicated from `Phillip's post in raspberrypi.org <https://www.raspberrypi.org/forums/viewtopic.php?t=91185>`_.

The documentation that comes with the MPL115A2 temperature and pressure sensor from Adafruit only gives C code for Arduino, which is less useful than might have been hoped. I've searched in vain for Python code for the Raspberry Pi.

After quite a long slog, I think I have it working. Gotchas along the way were the fact that SMBus function read_word_data() appears to assume little-endian data whereas the device presents it big-endian (SMBus documentation leaves quite a lot to be desired), and the knotty little problem of how to convert 16 bits 2's complement presented as a long into a float. The MPL115A2 datasheet was not exactly written for dummies, and I still can't figure how the definition of coefficient c12 corresponds with how you in fact have to interpret it.

Anyway here's my code. This post is not really asking a question (unless anyone can suggest any improvements or bug fixes), but rather in the hope that the next person trying to do it might have more success in a Google search than I did.

.. code-block:: python

        #!/usr/bin/python
        import time
        import smbus

        bus = smbus.SMBus(1)

        addr = 0x60

        # a0: 16 bits - 1 sign, 12 int, 3 frac
        a0 = (bus.read_byte_data(addr, 0x04) <<8) | \
              bus.read_byte_data(addr, 0x05)
        if a0 & 0x8000:
            a0d = -((~a0 & 0xffff) + 1)
        else:
            a0d = a0
        a0f = float(a0d) / 8.0
        print("a0 = 0x%4x %5d %4.3f" % (a0, a0d, a0f))
        
        # b1: 16 bits - 1 sign, 2 int, 13 frac
        b1 = (bus.read_byte_data(addr, 0x06) << 8 ) | \
              bus.read_byte_data(addr, 0x07)
        if b1 & 0x8000:
            b1d = -((~b1 & 0xffff) + 1)
        else:
            b1d = b1
        b1f = float(b1d) / 8192.0
        print("b1 = 0x%4x %5d %1.5f" % (b1, b1d, b1f))
        
        # b2: 16 bits - 1 sign, 1 int, 14 frac
        b2 = (bus.read_byte_data(addr, 0x08) << 8) | \
              bus.read_byte_data(addr, 0x09)
        if b2 & 0x8000:
            b2d = -((~b2 & 0xffff) + 1)
        else:
            b2d = b2
        b2f = float(b2d) / 16384.0
        print("b2 = 0x%4x %5d %1.5f" % (b2, b2d, b2f))
        
        # c12: 14 bits - 1 sign, 0 int, 13 frac
        # (Documentation in the datasheet is poor on this.)
        c12 = (bus.read_byte_data(addr, 0x0a) << 8) | \
               bus.read_byte_data(addr, 0x0b)
        if c12 & 0x8000:
            c12d = -((~c12 & 0xffff) + 1)
        else:
            c12d = c12
        c12f = float(c12d) / 16777216.0
        print("c12 = 0x%4x %5d %1.5f" % (c12, c12d, c12f))
        
        # Start conversion and wait 3mS
        bus.write_byte_data(addr, 0x12, 0x0)
        time.sleep(0.003)
        
        rawpres = (bus.read_byte_data(addr, 0x00) << 2) | \
               (bus.read_byte_data(addr, 0x01) >> 6)
        rawtemp = (bus.read_byte_data(addr, 0x02) << 2) | \
               (bus.read_byte_data(addr, 0x03) >> 6)
        
        print("\nRaw pres = 0x%3x %4d" % (rawpres, rawpres))
        print("Raw temp = 0x%3x %4d" % (rawtemp, rawtemp))
        
        pcomp = a0f + (b1f + c12f * rawtemp) * rawpres + b2f * rawtemp
        pkpa = pcomp / 15.737 + 50
        print("Pres = %3.2f kPa" % pkpa)
        
        temp = 25.0 - (rawtemp - 498.0) / 5.35
        print("Temp = %3.2f" % temp)

