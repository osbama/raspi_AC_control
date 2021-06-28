
.. highlight:: bash



.. role:: bash(code)
   :language: bash



IR in Raspbian
========================

With the latest Raspbian software in 2021, the recommended module to handle IR signal is gpio-ir instead of LIRC.

add the following lines to the end of :bash:`/boot/config.txt`

.. code-block :: bash

        dtoverlay=gpio-ir,gpio_pin=24
        dtoverlay=gpio-ir-tx,gpio_pin=23

   
install :bash:`ir-keytable` and then reboot. 

.. code-block :: bash

        sudo apt install ir-keytable
        sudo shutdown -r now

after the reboot, you should see following; 

.. code-block :: bash

        $ ls -l /dev/lirc*
        crw-rw---- 1 root video 251, 0 Aug 22 17:20 /dev/lirc0
        crw-rw---- 1 root video 251, 1 Aug 22 17:20 /dev/lirc1

We shall use `ir-ctl` command for recording and playing back the AC remote. Air conditioner remotes send every bit of data at each keypress, so the strategy and automation intended for TV remotes will not work.

For additional info;

.. code-block :: bash

        $ ir-ctl -f
        Receive features /dev/lirc0:
         - Device cannot receive
        Send features /dev/lirc0:
         - Device can send raw IR
         - IR scancode encoder
         - Set carrier
         - Set duty cycle

This tells me that ir-ctl will use /dev/lirc0 by default, and it is the IR LED.

.. code-block :: bash

        $ ir-ctl -d /dev/lirc1 -f
        Receive features /dev/lirc1:
         - Device can receive raw IR
         - Can report decoded scancodes and protocol
         - Can set receiving timeout min:1 microseconds max:1250000 microseconds
        Send features /dev/lirc1:
         - Device cannot send

This tells me that /dev/lirc1 is the receiver.

Record signals from remote
-----------------------------

You can record the IR signal from the remote using the following command

.. code-block :: bash

        ir-ctl -d /dev/lirc1 -r -t 1250000 >Remote_command.txt

This will read the pulse and space data from the remote to the Remote_command file.

The -d parameter tells ir-ctl command use /dev/lirc1 to read.

The -r parameter is for receiving

The -t command is for timeout. I set the maximum possible due to amount of data AC remote sends. 

Press the power button exactly once, then exit by pressing CTRL+C on the keyboard.

You can edit the created file, and remove the `timeout` line, in order to reduce the number of error logs.


.. warning ::
   Raw recording of IR sensor data is extremely sensitive to the environment. Care must be taken to prevent stray
   IR radiation from interfering with the recording. For this purpose, I recommend placing the remote very close
   to the receiver, and covering the setup with a thick material to provide shade from ambient IR. You might need 
   to repeat the process a few times until every part of the protocol is captured. 
   
