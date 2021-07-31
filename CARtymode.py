#!/usr/bin/python3
from config import (
    username,
    client_id,
    client_secret,
    app_redirect,
    scope,
    cached_token,
    target_devices,
)

import spotipy
import sys
import datetime
import time
import keyboard
import argparse
import signal
import requests
import threading
import logging

logging.basicConfig(level=logging.INFO)

from songs import Song
from songs.turnallthelightson import turnallthelightson
from songs.caramelldansen import caramelldansen

from cars import Car
from cars.corsa import corsa
from cars.corsastub import corsastub

logging.getLogger(__name__).setLevel(logging.DEBUG)
logging.getLogger("songs").setLevel(logging.DEBUG)
logging.getLogger("cars").setLevel(logging.DEBUG)

LOG = logging.getLogger(__name__)
## Fixed config, do not change

parser = argparse.ArgumentParser(
    description="Play songs on your car while giving a light show."
)

parser.add_argument(
    "target_device",
    help="On which Spotify device should the song play (spotify id)",
    choices=target_devices.keys(),
)

parser.add_argument(
    "car",
    help="On which Car should the lightshow play",
    choices=[c.__name__ for c in Car.__subclasses__()],
)

parser.add_argument(
    "song",
    help="Which song should play",
    choices=[c.__name__ for c in Song.__subclasses__()],
)


parser.add_argument(
    "--output-device",
    help="Override the default output device. Possible values depend on car. E.g. COM1, can0, vcan0, ..",
)

parser.add_argument(
    "--watch-keyboard",
    help="Press the time into song when pressing enter",
    action="store_true",
)

args = parser.parse_args()


target_device = target_devices[args.target_device]

car = None
for c in Car.__subclasses__():
    if c.__name__ == args.car:
        car = c(args.output_device)

song = None
for s in Song.__subclasses__():
    if s.__name__ == args.song:
        song = s(car)

## dynamic config starts here
token = None

try:
    token = spotipy.util.prompt_for_user_token(
        username,
        scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=app_redirect,
    )
except Exception as ex:
    LOG.info("Unable to fetch new spotify token. Using cached token")
    token = cached_token


LOG.info("Used spotify token: {token}".format(token=token))

sp = None
while sp is None:
    try:
        sp = spotipy.Spotify(auth=token)
        sp.current_user()
    except spotipy.exceptions.SpotifyException:
        print("Unable to authenticate to spotify")
        token = input("Please input a valid Spotify authn token:")
        sp = None

LOG.info(
    "Waiting for {spotify_device} to appear".format(spotify_device=args.target_device)
)
device_found = False
while not device_found:
    for device in sp.devices()["devices"]:
        LOG.debug(device)
        if device["id"] == target_device:
            # if not device["is_active"]:
            #     print("Target device is not active! Retrying.. ")
            #     continue

            device_found = True
            break
    time.sleep(0.5)
LOG.info("Device found")

started = True


def signal_handler(sig, frame):
    global started
    LOG.info("You pressed Ctrl+C!")
    LOG.info("Requesting to stop everything")
    started = False  # Signal the app to stop


signal.signal(signal.SIGINT, signal_handler)


foobar = datetime.datetime.now()


def printtimestamp():
    global foobar
    time_passed = datetime.datetime.now() - foobar

    minutes, seconds = divmod(time_passed.total_seconds(), 60)
    LOG.info(
        "{minutes:02d}:{seconds:06.3f} - You pressed ENTER!".format(
            minutes=int(minutes), seconds=seconds
        )
    )


if args.watch_keyboard:
    keyboard.add_hotkey("enter", printtimestamp, suppress=True, timeout=0.05)


car.start()
while started:
    lightshow = song.start(sp, target_device, offset="00:10.300")
    foobar = datetime.datetime.now()
    LOG.info("Waiting song to finish")
    lightshow.join()
    time.sleep(3)

LOG.info("Stopping the car")
car.stop()
