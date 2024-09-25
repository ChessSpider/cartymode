from pandas._libs.tslibs.timedeltas import Timedelta
from . import TimedAction, Song
import pandas as pd


class caramelldansen(Song):
    spotify_id = "spotify:track:7MwwPyZJ7UKFROj2oVnH6R"
    car = None

    def __init__(self, car):
        super().__init__()
        self.car = car

    def return_actions(self):
        actions = [
            {
                "00:00.000": self.car.turnallthelightson,
                "00:14.000": self.car.turnallthelightsoff,
            },
            self.timeseries(
                "00:16.700",
                duration_on=pd.Timedelta("300ms"),
                interval=pd.Timedelta("1300ms"),
                periods=4,
                action_on=self.car.highbeam.turnon,
                action_off=self.car.highbeam.turnoff,
            ),
            self.timeseries(
                "00:22.200",
                duration_on=pd.Timedelta("300ms"),
                interval=pd.Timedelta("1250ms"),
                periods=4,
                action_on=self.car.highbeam.turnon,
                action_off=self.car.highbeam.turnoff,
            ),
            self.timeseries(
                "00:28.000",
                duration_on=pd.Timedelta("150ms"),
                interval=pd.Timedelta("300ms"),
                periods=20,
                action_on=self.car.highbeam.turnon,
                action_off=self.car.highbeam.turnoff,
            ),
        ]
        return actions
