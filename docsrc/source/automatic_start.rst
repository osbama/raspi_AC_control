.. highlight:: bash


.. role:: bash(code)
   :language: bash



Setting up for automatic start
================================

After you download your script to your user directory, you can use `systemd` for starting it up automatically. 

Create a new `systemd` unit file called `ac_control.service`


.. code-block :: bash

   sudo vim /lib/systemd/system/ac_control.service 

Adding the following text:

.. code-block :: bash
   
   [Unit]
   Description=AC control service
   After=multi-user.target

   [Service]
   Type=idle
   ExecStart=/usr/bin/python3 /home/obm/source/environment_control/main.py 

   [Install]
   WantedBy=multi-user.target

This defines a new service called `ac_control` and we are requesting that it is launched once the multi-user environment is available. The `ExecStart` parameter is used to specify the command we want to run. The `Type` is set to `idle` to ensure that the `ExecStart` command is run only when everything else has loaded. Note that the paths are absolute and define the complete location of Python as well as the location of our Python script.

In order to store the script’s text output in a log file you can change the ExecStart line to:

.. code-block :: bash

   ExecStart=/usr/bin/python3 /home/obm/source/environment_control/main.py > /home/obm/ac_control.log 2>&1


The permission on the unit file needs to be set to 644 :

.. code-block :: bash
 
   sudo chmod 644 /lib/systemd/system/ac_control.service


Now the unit file has been defined we can tell systemd to start it during the boot sequence :

.. code-block :: bash

   sudo systemctl daemon-reload
   sudo systemctl enable ac_control.service
   sudo systemctl start ac_control.service

Reboot the Pi and your custom service should run:

.. code-block :: bash

   sudo reboot

