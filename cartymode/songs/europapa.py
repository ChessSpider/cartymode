from pandas._libs.tslibs.timedeltas import Timedelta
from . import TimedAction, Song
import pandas as pd


class europapa(Song):
    spotify_id = "spotify:track:0uHrMbMv3c78398pIANDqR"
    car = None

    def __init__(self, car):
        super().__init__()
        self.car = car

    def return_actions(self):
        actions = [
            {
                "00:00.000": self.car.turnallthelightson,
                "00:01.000": self.car.turnallthelightsoff,
            },
            {
                "00:05.000": self.car.turnallthelightson,
                "00:06.000": self.car.turnallthelightsoff,
                "00:15.000": self.car.turnallthelightson,
                "00:20.000": self.car.turnallthelightsoff,
            }
        ]
        return actions
