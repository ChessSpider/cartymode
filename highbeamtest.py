#!/usr/bin/python

import time
import threading
import copy
import can
from can import Message
import signal
import sys

# messages
control = [  # control messages seem to be multiple in a loop
    # These messages apparently tell the BCM-module that it should listen to commands
    Message(
        arbitration_id=0x552,
        data=[0x0C, 0x25, 0x44, 0x00, 0x00, 0x00, 0x01, 0x00],
        extended_id=False,
    ),
    Message(
        arbitration_id=0x552,
        data=[0x0D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00],
        extended_id=False,
    ),
    Message(
        arbitration_id=0x552,
        data=[0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00],
        extended_id=False,
    ),
    Message(
        arbitration_id=0x552,
        data=[0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00],
        extended_id=False,
    ),
    Message(
        arbitration_id=0x552,
        data=[0x13, 0x08, 0x7F, 0x00, 0x00, 0x00, 0x01, 0x00],
        extended_id=False,
    ),
]
start = Message(
    arbitration_id=0x252,
    data=[0x07, 0xAA, 0x03, 0x0C, 0x0D, 0x0F, 0x12, 0x13],
    extended_id=False,
)
end = Message(arbitration_id=0x999, data=[0x00], extended_id=False)

# Base comamand msgs for BCM-commands
base = Message(
    arbitration_id=0x252,
    data=[0x06, 0xAE, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00],
    extended_id=False,
)

# front of car
highbeamon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x04, 0x04, 0x00, 0x00, 0x00],
    extended_id=False,
)
highbeamoff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00],
    extended_id=False,
)
lowbeamon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x02, 0x02, 0x00, 0x00, 0x00],
    extended_id=False,
)
lowbeamoff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00],
    extended_id=False,
)
frontfogon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00],
    extended_id=False,
)
frontfogoff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00],
    extended_id=False,
)

# side of car
leftsignalon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x00],
    extended_id=False,
)
leftsignaloff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00],
    extended_id=False,
)
rightsignalon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x08, 0x00],
    extended_id=False,
)
rightsignaloff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00],
    extended_id=False,
)

# rear of car
centrebrakeon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00],
    extended_id=False,
)
centrebrakeoff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00],
    extended_id=False,
)
parklighton = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00],
    extended_id=False,
)
parklightoff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00],
    extended_id=False,
)
rearfogon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x40, 0x40, 0x00, 0x00, 0x00],
    extended_id=False,
)
rearfogoff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00],
    extended_id=False,
)
reverseon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x00],
    extended_id=False,
)
reverseoff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00],
    extended_id=False,
)
licenseplateon = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x20, 0x20, 0x00, 0x00, 0x00],
    extended_id=False,
)
licenseplateoff = Message(
    arbitration_id=0x252,
    data=[0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00],
    extended_id=False,
)


# can interfaces
can0 = can.interface.Bus(bustype="socketcan", channel="can0", bitrate=500000)

# Helper function to create BCM command messages
def preparemsg(a, b):
    new = copy.deepcopy(a)
    for i in range(len(new)):
        new.data[i] |= b.data[i]
    return new

    # control logic; allow the application to stop gracefully


started = True


def signal_handler(sig, frame):
    global started
    print("You pressed Ctrl+C!")
    print("Requesting to stop everything")
    started = False  # Signal the app to stop


signal.signal(signal.SIGINT, signal_handler)

# continuously send keep control messages
def keepcontrol():
    global started
    while started:
        for controlmessage in control:
            can0.send(controlmessage)
            time.sleep(0.01)  # delay between contrl message salvo (checked)
        time.sleep(0.2)  # delay between salvo (checked)


keepcontrol = threading.Thread(target=keepcontrol)
keepcontrol.start()

on = None
off = None

while on == None or off == None:
    print()
    print("Please set the 'on' and 'off' variable to an instance of can.Message.")
    print("Press c to continue")
    print("Example:")
    print(" on  = preparemsg(base,highbeamon)")
    print(" off = preparemsg(base,highbeamoff)")
    print()
    print("Available presets:")
    print(" Lights front: highbeam,lowbeam,frontfog")
    print(" Lights side : leftsignal,rightsignal")
    print(" lights rear : centrebrake,parklight,rearfog,reverse,licenseplate")
    print()
    import pdb

    pdb.set_trace()

    # Start the control!
can0.send(start)  # take control command
while started:  # repeat the on/off sequence times
    print("aan")
    can0.send(on)
    time.sleep(1)
    print("uit")
    can0.send(off)
    time.sleep(1)

print("closing")
keepcontrol.join()

can0.send(end)

print("stopped")
