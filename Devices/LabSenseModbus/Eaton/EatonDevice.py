import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

sys.path.insert(1, os.path.abspath("../../.."))
from EatonClient import EatonClient
from Devices.Device import Device

class EatonDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval):
        super(EatonDevice, self).__init__(sinterval)
        self.name = name
        self.channels = channels
        self.devicename = "Eaton"
        self.client = EatonClient(name, IP, PORT, channels)

if __name__ == "__main__":

    # Import sinks and configReader
    import LabSenseHandler.configReader as configReader
    from DataSinks.DataSink import DataSink

    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Eaton device")
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from Eaton.")
    args = parser.parse_args()

    # Read configuration
    config = configReader.config

    # Create communication threads
    threads = []

    device_name = "Eaton"

    # Initialize the Eaton Device
    device = EatonDevice(args.name, args.IP, args.PORT,
            config[device_name]["channels"], config[device_name]["sinterval"])
    threads.append(device)

    # Attach the sinks
    device_config = config[device_name]
    for sink in ["SensorAct", "Cosm", "Stdout"]:
        if device_config[sink]:
            interval = device_config[sink + "Interval"]
            queue = Queue.Queue()
            device.attach(queue)
            dataSink = DataSink.dataSinkFactory(sink, config[sink], queue, interval)
            dataSink.registerDevice(device_name, device_config)
            threads.append(dataSink)

    print "Number of threads: ", len(threads)
    for thread in threads:
        thread.daemon = True
        thread.start()

    while True:
        for thread in threads:
            if not thread.isAlive():
                sys.exit("Thread died. Exiting Program")


    #while len(threads) > 0:
        #try:
            #threads = [t.join(1) for t in threads if t is not None and
                       #t.isAlive()]
        #except KeyboardInterrupt:
            #print "Ctrl-c received! Sending kill to threads..."
            #for thread in threads:
                #thread.kill_received = True

    #for thread in threads:
        #if not thread.isAlive():
            #print "A thread just died!"

    #for thread in threads:
        #while thread.isAlive():
            #thread.join(5)
