from pandas._libs.tslibs.timedeltas import Timedelta
from . import TimedAction, Song
import pandas as pd


class europapa(Song):
    spotify_id = "spotify:track:0uHrMbMv3c78398pIANDqR"
    car = None

    def __init__(self, car):
        self.car = car

    def return_actions(self):
        actions = [
            {
                "00:00.000": self.car.turnallthelightson,
                "02:41.000": self.car.turnallthelightsoff,
            }
        ]
        return actions
