LabSense
========

This project involves creating a sensing platform that can measure many
different characteristics about a lab (i.e. ambient temperature, 
electricity, water, occupancy). The project also focuses on making the data 
available with a user-intuitive interface.

LabSenseServer
--------------

LabSenseServer contains the code running on the server, which communicates
with a plug computer (Guru plug) that is present in every laboratory that
is equipped. Each guru plug talks to several different sensors through a
multitude of different protocols (i.e. Zigbee, Bluetooth, Zwave).

This server will also host a website through which users can view the
different sensor outputs in an intuitive interface. 

The server will also serve a public api that others can use to read the
data from the different sensors. Other applications can then process the
data and perform their own analysis of the streaming data.

Dependency:

* [Django 1.3.1](https://www.djangoproject.com/download/)

------------------------------------------------------------------------------

LabSenseZwave
--------------

LabSenseZwave contains the code running on the guruplug. This code 
specifically focuses on the zwave aspect of the guruplug. The open-zwave 
project is used for the zwave implementation. The Main.cpp file contains the
code that receives notifications from the Homeseer Multisensor, the Aeon 
Labs Door/Window Sensor, and the Aeon Labs SmartSwitch. 

Zeromq is used as a transport layer to send the data from the 
LabSenseZwave executable to a python process that sends the data to SensorSafe.
This is meant to decouple the Zwave data retrieval from the possible slower
Http requests and network latency. 

Dependency:

* [Open-zwave](http://code.google.com/p/open-zwave/)
* [Zeromq](http://www.zeromq.org/intro:get-the-software)

------------------------------------------------------------------------------

Hardware Requirements
---------------------
This software is running on a [Guruplug Server](http://www.globalscaletechnologies.com/t-guruplugdetails.aspx) with an
[Aeon Labs Z-stick](http://www.aeon-labs.com/site/products/view/2/). 
The sensors that interact with the Z-stick include:

* [Aeon Labs Door/Window Sensor](http://www.aeon-labs.com/site/products/view/1/)
* [Homeseer MultiSensor](http://store.homeseer.com/store/HomeSeer-HSM100-S2-Z-Wave-Multi-Sensor-P1189C57.aspx)
* [Aeon Labs SmartSwitch](http://www.aeon-labs.com/site/products/view/5/)

------------------------------------------------------------------------------

Installation
--------------

1. Install Zeromq by following directions at http://www.zeromq.org/intro:get-the-software
2. Install python bindings by following directions at http://www.zeromq.org/bindings:python
3. Install needed development headers for open-zwave:

    <pre>
    sudo apt-get install libudev-dev
    </pre>

4. Get the open-zwave source code using svn by running:

    <pre>
    svn checkout http://open-zwave.googlecode.com/svn/trunk/ open-zwave/
    </pre>

5. Navigate to open-zwave/cpp/examples/linux/
6. Get the source code for this project using git or download it:

    <pre>
    git clone git@github.com:jtsao22/LabSense.git
    </pre>

    The LabSense Project should now be at open-zwave/cpp/examples/linux/LabSense.

7. Navigate to LabSense/LabSenseZwave/
8. Pair the Z-stick with the sensors:

    1. Push the button on the Z-stick. The light on the Z-stick should blink. 
    2. Push the button on the sensor. The light on the Z-stick should stay lit for a few seconds and then start blinking again. 
    3. The sensor has been paired and the Z-stick is ready for the next sensor. Start at step 2 for the next sensor. 
    4. When all sensors have been paired, push the button on the Z-stick and the light should stop blinking.

8. Make the code and run the executable

    <pre>
    make 
    ./LabSenseZwave [serial port]
    </pre>

    To figure out what serial port, please plug the Z-stick into the Guruplug and run dmesg. A line similar to the following should specify the port:

    <pre>
    "cp210x converter now attached to [serial port]"
    </pre>

    Unless other usb devices are plugged in, usually the serial port is /dev/ttyUSB0. 

The previous steps are used for local viewing of the data coming off the sensors. If an online graphical view of the
sensor data is required, more code has been implemented to send the data to [SensorSafe](https://128.97.93.29/):

1. Register for a SensorSafe account and take note of the API key.
2. To send the data to SensorSafe, run the python script sendToSensorSafe.py while running the LabSenseZwave
executable:

    <pre>
    python sendToSensorSafe.py [api-key] -f [frequency]
    </pre>

    [api-key] is the API key given during SensorSafe registration.
    [frequency] is optional and specifies how often to send data to SensorSafe.
    The usage details can be found by using "-h" or "--help"

    (Either run this in a separate ssh session/terminal or run one of the processes in the background).

    To see more information about the inner workings of sendToSensorSafe.py, 
    you can use pydoc (installed with python):

    <pre>
    pydoc sendToSensorSafe
    </pre>

3. The script will send to SensorSafe as soon as all variables have been initialized (temperature, luminance, and
motion_timeout), which make take some time depending on the wake-up interval of the Homeseer Multisensor (programmed to
be every 6 minutes).
Upon successful upload to SensorSafe, a message similar to the following will show up:

    <pre>
    200 OK
    [('transfer-encoding', 'chunked'), ('vary', 'Accept-Encoding'), ('server', 'Apache/2.2.11 (Ubuntu) mod_ssl/2.2.11
    OpenSSL/0.9.8g mod_wsgi/2.3 Python/2.6.2'), ('connection', 'close'), ('date', 'Tue, 10 Apr 2012 19:47:03 GMT'),
    ('access-control-allow-origin', '*'), ('content-type', 'text/html; charset=utf-8')]
    Upload successful (Collection name: sandbox, Requested by sandbox
    </pre>

4. You can then see the data on SensorSafe by signing in, pressing access data, selecting data channels, and pressing Show Data. 

------------------------------------------------------------------------------

By Jason Tsao
