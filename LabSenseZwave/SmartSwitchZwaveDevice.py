import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

from SmartSwitchZwaveClient import SmartSwitchZwaveClient

sys.path.insert(0, os.path.abspath(".."))
from LabSenseModbus.common.Device import Device 
from LabSenseModbus.common.Device import Device
from LabSenseModbus.common.DataSinks.StdoutSink import StdoutSink
from LabSenseModbus.common.DataSinks.SensorActSink import SensorActSink
from LabSenseModbus.common.DataSinks.CosmSink import CosmSink 

import LabSenseHandler.configReader as configReader

class SmartSwitchZwaveDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval):
        super(SmartSwitchZwaveDevice, self).__init__(sinterval)
        self.name = name
        self.channels = channels
        self.devicename = "SmartSwitch"
        self.client = SmartSwitchZwaveClient(name, IP, PORT, channels)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of SmartSwitch device")
    parser.add_argument("IP", help="IP address for SmartSwitch")
    parser.add_argument("PORT", help="Port for SmartSwitch")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from SmartSwitch.")
    args = parser.parse_args()

    # Read configuration
    config = configReader.config

    # Create communication threads
    threads = []

    name = "SmartSwitch"

    # Initialize the SmartSwitch Device thread
    device = SmartSwitchZwaveDevice(args.name, args.IP, args.PORT,
            config[name]["channels"], config[name]["sinterval"])
    threads.append(device)

    if config[name]["SensorAct"]:
        sensorActInterval = config[name]["SensorActInterval"]
        sensorActQueue = Queue.Queue();
        sensorActSink = SensorActSink(config,
                sensorActQueue, sensorActInterval)
        device.attach(sensorActQueue)
        threads.append(sensorActSink)

    if config[name]["Cosm"]:
        cosmInterval = config[name]["CosmInterval"]
        cosmQueue = Queue.Queue()
        cosmSink = CosmSink(config, cosmQueue, cosmInterval)
        device.attach(cosmQueue)
        threads.append(cosmSink)

    if config[name]["Stdout"]:
        stdoutInterval = config[name]["StdoutInterval"]
        stdoutQueue = Queue.Queue()
        stdoutSink = StdoutSink(config, stdoutQueue,
                stdoutInterval)
        device.attach(stdoutQueue)
        threads.append(stdoutSink)

    print "Number of threads: ", len(threads)

    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        while thread.isAlive():
            thread.join(5)