import time
from . import Car
import serial
import serial.tools.list_ports


class nullcar(Car):
    """
    doesnt do anything at all
    """

    highbeam = None
    lowbeam = None
    leftsignal = None
    rightsignal = None
    frontfog = None
    parklight = None

    def __init__(self, output_device=None):

        pass

    def turnsignalson(self, sleep=0):
        pass
        if sleep:
            time.sleep(sleep)

    def turnsignalsoff(self, sleep=0):
        pass
        if sleep:
            time.sleep(sleep)

    def turnallthelightson(self, sleep=0):
        pass
        if sleep:
            time.sleep(sleep)

    def turnallthelightsoff(self, sleep=0):
        pass
        if sleep:
            time.sleep(sleep)

    def send(self):
        pass

    def stop(self):
        pass