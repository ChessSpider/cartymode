import time
from . import Car
import serial
import serial.tools.list_ports


class corsastub(Car):
    """
    Communicates with the arduino/esp32 fake __class__.ino via rs232
    """

    class light(object):
        def __init__(self, lightstring, serialconn):
            self.lightstring = lightstring
            self.conn = serialconn

        def turnon(self, sleep=0):
            self.conn.write((self.lightstring + "h").encode())
            self.conn.flush()
            if sleep:
                time.sleep(sleep)

        def turnoff(self, sleep=0):
            self.conn.write((self.lightstring + "l").encode())
            self.conn.flush()
            if sleep:
                time.sleep(sleep)

        def send(self):
            pass

    highbeam = None
    lowbeam = None
    leftsignal = None
    rightsignal = None
    frontfog = None
    parklight = None

    def __init__(self, output_device=None):

        comports = serial.tools.list_ports.comports()
        comname = None
        if output_device is not None:
            comname = output_device
        elif len(comports) == 1:
            comname = comports[0].name
        else:
            raise Exception(
                "Cannot find connport '{comports}'!".format(comports=",".join(comports))
            )

        serialconn = serial.Serial(comname, 115200)

        self.conn = serialconn
        self.highbeam = __class__.light("hb", serialconn)
        self.lowbeam = __class__.light("lb", serialconn)
        self.leftsignal = __class__.light("ls", serialconn)
        self.rightsignal = __class__.light("rs", serialconn)
        self.frontfog = __class__.light("ff", serialconn)
        self.parklight = __class__.light("pl", serialconn)

    def turnsignalson(self, sleep=0):
        self.leftsignal.turnon()
        self.rightsignal.turnon()
        if sleep:
            time.sleep(sleep)

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

    def send(self):
        pass

    def stop(self):
        self.conn.close()