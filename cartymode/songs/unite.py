from pandas._libs.tslibs.timestamps import Timestamp
from . import TimedAction, Song
import pandas as pd


class unite(Song):
    spotify_id = "spotify:track:6LOOqW1iQwYNWF0Gtilu7H"
    car = None

    def __init__(self, car):
        super().__init__()
        self.car = car

    def return_actions(self):
        actions = [
            {
                "00:00.000": self.car.turnallthelightson,
                "00:00.500": self.car.turnallthelightsoff,
                "00:06.300": self.car.lowbeam.turnon,
                "00:06.800": self.car.highbeam.turnon,
                "00:07.300": self.car.turnsignalson,
                "00:08.000": self.car.turnallthelightsoff,
                "00:09.700": self.car.lowbeam.turnon,
                "00:10.200": self.car.highbeam.turnon,
                "00:10.700": self.car.turnsignalson,
                "00:11.000": self.car.turnallthelightsoff,
                "00:12.700": self.car.lowbeam.turnon,
                "00:13.200": self.car.highbeam.turnon,
                "00:13.700": self.car.turnsignalson,
                "00:14.000": self.car.turnallthelightsoff,
            },
            self.timeseries(
                "00:19.300",
                duration_on=pd.Timedelta(milliseconds=200),
                interval=pd.Timedelta(milliseconds=350),
                periods=4,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(
                "00:22.400",
                duration_on=pd.Timedelta(milliseconds=200),
                interval=pd.Timedelta(milliseconds=350),
                periods=4,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(
                "00:25.500",
                duration_on=pd.Timedelta(milliseconds=200),
                interval=pd.Timedelta(milliseconds=350),
                periods=4,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(
                "00:28.600",
                duration_on=pd.Timedelta(milliseconds=200),
                interval=pd.Timedelta(milliseconds=350),
                periods=4,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(
                "00:31.700",
                duration_on=pd.Timedelta(milliseconds=200),
                interval=pd.Timedelta(milliseconds=350),
                periods=4,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(
                "00:34.800",
                duration_on=pd.Timedelta(milliseconds=200),
                interval=pd.Timedelta(milliseconds=350),
                periods=4,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(
                "00:37.900",
                duration_on=pd.Timedelta(milliseconds=200),
                interval=pd.Timedelta(milliseconds=350),
                periods=4,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(
                "00:41.000",
                duration_on=pd.Timedelta(milliseconds=200),
                interval=pd.Timedelta(milliseconds=350),
                periods=4,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            {
                "00:44.500": self.car.turnallthelightson,
                "00:44.700": self.car.turnallthelightsoff,
                "00:46.000": self.car.turnallthelightson,
                "00:46.200": self.car.turnallthelightsoff,
                "00:47.600": self.car.turnallthelightson,
                "00:47.800": self.car.turnallthelightsoff,
                "00:49.300": self.car.turnallthelightson,
                "00:49.500": self.car.turnallthelightsoff,
                "00:50.800": self.car.turnallthelightson,
                "00:51.000": self.car.turnallthelightsoff,
                "00:52.300": self.car.turnallthelightson,
                "00:52.500": self.car.turnallthelightsoff,
            },
        ]
        return actions
