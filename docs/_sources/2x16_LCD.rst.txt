
.. highlight:: python

I2C 2x16 LCD
=================

The following are `excerpts from this article  <https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/>`_ 

2x16 LCD with I2C uses only two pins to communicate with Raspberry instead of the 16 in parallel communication. This bus can also be shared with other sensors. In this project I use `2x16 I2C LCD <https://funduino.de/nr-19-i%C2%B2c-display>`_ 

Connecting an LCD with an I2C backpack is pretty self-explanatory. Connect the SDA pin on the Pi to the SDA pin on the LCD, and the SCL pin on the Pi to the SCL pin on the LCD. The ground and Vcc pins will also need to be connected. Most LCDs can operate with 3.3V, but they’re meant to be run on 5V, so connect it to the 5V pin of the Pi if possible.


``i2cdetect -y 1`` shows the I2C address of my LCD is 27.

I found a Python I2C library that has a good set of functions and works pretty well. This library was originally posted `here <http://www.recantha.co.uk/blog/?p=4849>`_, then expanded and improved by GitHub user `DenisFromHR <https://gist.github.com/DenisFromHR/cc863375a6e19dce359d>`_. This is in ``LCD/I2C_LCD_driver.py`` directory. 

There are a couple things you may need to change in the code above, depending on your set up. On line 19 there is a function that defines the port for the I2C bus. Older Raspberry Pi’s used port 0, but newer models use port 1. Unless you have something older than 3, use port 1.

Next, put the I2C address of your LCD in line 22 of the library code. For example, my I2C address is 27, so I’ll change line 22 to ``ADDRESS = 0x27``.

Write to the Display
---------------------

The following is a bare minimum “Hello World!” program to demonstrate how to initialize the LCD:


.. code-block:: python

        import I2C_LCD_driver
        from time import *

        mylcd = I2C_LCD_driver.lcd()

        mylcd.lcd_display_string("Hello World!", 1)

Position the Text
------------------

The function ``mylcd.lcd_display_string()`` prints text to the screen and also lets you chose where to position it. The function is used as `mylcd.lcd_display_string("TEXT TO PRINT", ROW, COLUMN)``. For example, the following code prints “Hello World!” to row 2, column 3:

.. code-block:: python

        import I2C_LCD_driver
        from time import *

        mylcd = I2C_LCD_driver.lcd()

        mylcd.lcd_display_string("Hello World!", 2, 3)

On a 16×2 LCD, the rows are numbered 1 – 2, while the columns are numbered 0 – 15. So to print “Hello World!” at the first column of the top row, you would use mylcd.lcd_display_string("Hello World!", 1, 0).

Clear the Screen
-----------------

The function ``mylcd.lcd_clear()`` clears the screen:

.. code-block:: python

        import I2C_LCD_driver
        from time import *

        mylcd = I2C_LCD_driver.lcd()

        mylcd.lcd_display_string("This is how you", 1)
        sleep(1)

        mylcd.lcd_clear()

        mylcd.lcd_display_string("clear the screen", 1)
        sleep(1)
        
        mylcd.lcd_clear()

Blinking Text
---------------

We can use a simple while loop with the mylcd.lcd_display_string() and mylcd.lcd_clear() functions to create a continuous blinking text effect:

.. code-block:: python

        import time
        import I2C_LCD_driver
        mylcd = I2C_LCD_driver.lcd()

        while True:
            mylcd.lcd_display_string(u"Hello world!")
            time.sleep(1)
            mylcd.lcd_clear()
            time.sleep(1)

You can use the ``time.sleep()`` function on line 7 to change the time (in seconds) the text stays on. The time the text stays off can be changed in the time.sleep() function on line 9. To end the program, press Ctrl-C.

Print the Date and Time
--------------------------

The following program prints the current date and time to the LCD:


.. code-block:: python

        import I2C_LCD_driver
        import time
        mylcd = I2C_LCD_driver.lcd()
        
        
        while True:
            mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
        
            mylcd.lcd_display_string("Date: %s" %time.strftime("%m/%d/%Y"), 2)


Scroll Text Right to Left Continuously
------------------------------------------

This program will scroll a text string from the right side of the LCD to the left side and loop continuously:

.. code-block:: python

        import I2C_LCD_driver
        from time import *

        mylcd = I2C_LCD_driver.lcd()

        str_pad = " " * 16
        my_long_string = "This is a string that needs to scroll"
        my_long_string = str_pad + my_long_string

        while True:
            for i in range (0, len(my_long_string)):
                lcd_text = my_long_string[i:(i+16)]
                mylcd.lcd_display_string(lcd_text,1)
                sleep(0.4)
                mylcd.lcd_display_string(str_pad,1)
