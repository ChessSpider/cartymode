#!/usr/bin/python

import can
import time
from cars.corsa import corsa
import signal

can0 = can.interface.Bus(bustype="socketcan", channel="can0", bitrate=500000)

car = corsa(can0)
car.start()

started = True


def signal_handler(sig, frame):
    global started
    print("You pressed Ctrl+C!")
    print("Requesting to stop everything")
    started = False  # Signal the app to stop


signal.signal(signal.SIGINT, signal_handler)

while started:
    print("highbeam")
    car.highbeam.turnon(2)
    print("lowbeam")
    car.lowbeam.turnon(2)
    print("signals")
    car.leftsignal.turnon()
    car.rightsignal.turnon(2)
    print("frontfog")
    car.frontfog.turnon(10)
    print("all off")
    car.highbeam.turnoff()
    car.lowbeam.turnoff()
    car.frontfog.turnoff()
    car.leftsignal.turnoff()
    car.rightsignal.turnoff(5)

car.stop()
