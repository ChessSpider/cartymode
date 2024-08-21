import os
import can
from can import Message
import time
import copy
import threading

from . import Car


class kiacarens(Car):
    class light:
        car = None
        on = None
        off = None

        def __init__(self, car, on=None, off=None):

            self.car = car
            self.on = on
            self.off = off

        @staticmethod
        def mergecanmsg(a, b):
            new = copy.deepcopy(a)
            for i in range(len(new)):
                new.data[i] |= b.data[i]
            return new

        def turnon(self, sleep=0):
            self.car._cmd = self.mergecanmsg(self.car._cmd, self.on)
            if sleep > 0:
                self.car.send()
                time.sleep(sleep)

        def turnoff(self, sleep=0):
            # First we figure out which bit is actually set off compared to the on comand
            offbyte = bytes(a ^ b for (a, b) in zip(self.on.data, self.off.data))
            # Then we need to get a bytearray which would only turnthat byte off
            off = bytes(a ^ b for (a, b) in zip(offbyte, bytearray(b"\xFF" * 8)))
            # Last but not least, we AND it to current command to make sure we only disable whats needed
            newdata = bytes(a & b for (a, b) in zip(self.car._cmd.data, off))

            self.car._cmd.data = newdata
            if sleep > 0:
                self.car.send()
                time.sleep(sleep)

        def send(self):
            self.car.send()

    can = None  # Can interface
    started = False  #

    def __init__(self, output_device=None, configfile="kiacarens.settings"):
        self.can = can.interface.Bus(
            bustype="socketcan",
            channel="can0" if output_device is None else output_device,
            bitrate=500000,
        )
        self.load(configfile)

    def load(self, configfilename):
        def _createcanmsg(canmsg):
            (id, data) = canmsg.split("-")

            return can.Message(
                arbitration_id=int(id.strip()[2:].encode(), base=16),
                data=bytearray.fromhex(data.strip()[2:]),
                extended_id=False,
            )

        settings = open(os.path.dirname(__file__) + "/"+ configfilename, "r")
        for line in settings:
            (key, value) = line.split("=")
            items = key.split(".")  # index 1 = variable name, index 2 = on/off
            if key.startswith("light."):
                if len(items) != 3:
                    raise ValueError(
                        "Error loading settings; invalid length " + items[1]
                    )
                selectedlight = getattr(self, items[1])
                if selectedlight == None:
                    selectedlight = self.light(self)
                    setattr(self, items[1], selectedlight)
                canmsg = _createcanmsg(value)
                setattr(selectedlight, items[2].strip(), canmsg)
            elif key.startswith("bcm"):
                if len(items) != 3:
                    raise ValueError(
                        "Error loading settings; invalid length " + items[1]
                    )
                t = getattr(self, items[1])
                canmsg = _createcanmsg(value)
                index = int(items[2].strip())
                if index > 0 or isinstance(t, list):
                    if not isinstance(t, list):
                        t = [t]
                    t.insert(index, canmsg)
                else:
                    t = canmsg

                setattr(self, items[1], t)

    _cmd = None  # The command currently being built
    _previouscmd = None  # Last command executed
    _recurringmsg = None  # A recurring message for the BCM module for reasons unknown
    _controlmsgs = []
    _startmsg = None
    _stopmsg = None
    # Base comamand msgs for BCM-commands
    _basecmdmsg = None

    # front of car
    highbeam = None
    lowbeam = None
    frontfog = None

    # side of car
    leftsignal = None
    rightsignal = None

    # rear of car
    centrebrake = None
    parklight = None
    rearfog = None
    reverse = None
    licenseplate = None

    def turnsignalson(self, sleep=0):
        self.leftsignal.turnon()
        self.rightsignal.turnon(sleep)
        if sleep:
            time.sleep()

    def turnsignalsoff(self, sleep=0):
        self.leftsignal.turnoff()
        self.rightsignal.turnoff()
        if sleep:
            time.sleep(sleep)

    def turnallthelightson(self, sleep=0):
        self.highbeam.turnon()
        self.lowbeam.turnon()
        self.leftsignal.turnon()
        self.rightsignal.turnon()
        self.frontfog.turnon()
        self.parklight.turnon()
        if sleep:
            time.sleep(sleep)

    def turnallthelightsoff(self, sleep=0):
        self.highbeam.turnoff()
        self.lowbeam.turnoff()
        self.leftsignal.turnoff()
        self.rightsignal.turnoff()
        self.frontfog.turnoff()
        self.parklight.turnoff()
        if sleep:
            time.sleep(sleep)

    def getfront(self):
        return [self.highbeam, self.lowbeam, self.frontfog]

    def getside(self):
        return [self.leftsignal, self.rightsignal]

    def getrear(self):
        return [
            self.centrebrake,
            self.parklight,
            self.rearfog,
            self.reverse,
            self.licenseplate,
        ]

    def start(self):
        self.started = True
        self._control = [
            threading.Thread(target=self.keepcontrol),
            threading.Thread(target=self.recurring),
        ]
        [t.start() for t in self._control]
        time.sleep(0.1)
        self.can.send(self._startmsg)
        self.resetcommand()
        self._previouscmd = None

    def recurring(self):
        while self.started:
            self.can.send(self._recurringmsg)
            time.sleep(0.8)

    def keepcontrol(self):
        while self.started:
            for controlmessage in self._controlmsgs:
                self.can.send(controlmessage)
                time.sleep(0.01)  # delay between contrl message salvo (checked)
            time.sleep(0.2)  # delay between salvo (checked)

    def send(self):
        if self.started == False:
            raise Exception("Please run start() first")
        try:
            self._previouscmd = self._cmd
            self.can.send(self._previouscmd)
        except can.CanError as ex:
            print("Error while sending! %s," % (str(ex),))

        # self.resetcommand()

    def resetcommand(self):
        self._cmd = copy.deepcopy(self._basecmdmsg)

    def stop(self):
        self.can.send(self._stopmsg)
        self.started = False
        self.can.send(self._stopmsg)
        [t.join() for t in self._control]
