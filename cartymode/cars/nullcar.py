import time
from . import Car
import serial
import serial.tools.list_ports


class nullcar(Car):
    """
    doesnt do anything at all
    """

    class fakelight:
        def turnon(self,sleep=0):
            if sleep > 0:
                time.sleep(sleep)

        def turnoff(self):
            pass

        def send(self):
            pass

    # front of car
    highbeam = fakelight()
    lowbeam = fakelight()
    frontfog = fakelight()

    # side of car
    leftsignal = fakelight()
    rightsignal = fakelight()

    # rear of car
    centrebrake = fakelight()
    parklight = fakelight()
    rearfog = fakelight()
    reverse = fakelight()
    licenseplate = fakelight()

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