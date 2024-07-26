from pandas._libs.tslibs.timestamps import Timestamp
from . import TimedAction, Song
import pandas as pd


class turnallthelightson(Song):
    spotify_id = "spotify:track:5Ue25r0VGvZR7vaw3iB0gZ"
    car = None

    def __init__(self, car):
        self.car = car

    def return_actions(self):
        actions = [
            {  # MM:SS:MS
                "00:00.000": self.car.turnallthelightson,
                "00:01.000": self.car.turnallthelightsoff,
                # Start normal beat; 0.4 seconds on, 0.3 seconds off
                "00:01.300": self.car.lowbeam.turnon,
                "00:01.700": self.car.lowbeam.turnoff,
                "00:02.000": self.car.lowbeam.turnon,
                "00:02.400": self.car.lowbeam.turnoff,
                # Extra wait = 0.6 seconds
                "00:03.000": self.car.lowbeam.turnon,
                "00:03.400": self.car.lowbeam.turnoff,
                "00:03.700": self.car.lowbeam.turnon,
                "00:04.100": self.car.lowbeam.turnoff,
                # Extra wait
                "00:04.700": self.car.lowbeam.turnon,
                "00:05.100": self.car.lowbeam.turnoff,
                "00:05.400": self.car.lowbeam.turnon,
                "00:05.800": self.car.lowbeam.turnoff,
                # Extra extra wait = 0.8 seconds
                "00:06.600": self.car.lowbeam.turnon,
                "00:07.000": self.car.lowbeam.turnoff,
                "00:07.300": self.car.lowbeam.turnon,
                "00:07.700": self.car.lowbeam.turnoff,
                # Extra wait
                "00:08.300": self.car.lowbeam.turnon,
                "00:08.700": self.car.lowbeam.turnoff,
                "00:09.000": self.car.lowbeam.turnon,
                "00:09.400": self.car.lowbeam.turnoff,
                # Extra extra wait
                "00:10.200": self.car.lowbeam.turnon,
                "00:10.600": self.car.lowbeam.turnoff,
                "00:10.900": self.car.lowbeam.turnon,
                "00:11.300": self.car.lowbeam.turnoff,
                # Extra extra wait
                "00:12.100": self.car.lowbeam.turnon,
                "00:12.500": self.car.lowbeam.turnoff,
                "00:12.800": self.car.lowbeam.turnon,
                "00:13.200": self.car.lowbeam.turnoff,
            },
            {
                # "specials" in the song , like the "uh-oh ah-ah!"
                "00:04.100": self.car.turnsignalson,
                "00:04.300": self.car.turnsignalsoff,
                "00:04.500": self.car.turnsignalson,
                "00:04.700": self.car.turnsignalsoff,
                # next uh-oh ah-ah
                "00:07.700": self.car.turnsignalson,
                "00:07.900": self.car.turnsignalsoff,
                "00:08.100": self.car.turnsignalson,
                "00:08.300": self.car.turnsignalsoff,
                # next uh-oh ah-ah
                "00:11.200": self.car.turnsignalson,
                "00:11.400": self.car.turnsignalsoff,
                "00:11.600": self.car.turnsignalson,
                "00:11.800": self.car.turnsignalsoff,
            },
            {  ## -- normal song continues
                # (Take off your) Shoes shoes shoes..
                "00:16.000": self.car.lowbeam.turnon,
                "00:16.600": self.car.turnsignalson,
                "00:17.000": self.car.highbeam.turnon,
                "00:17.500": [
                    self.car.lowbeam.turnoff,
                    self.car.turnsignalsoff,
                    self.car.highbeam.turnoff,
                ],
                # (bring out the) Booze booze booze..
                "00:19.800": self.car.lowbeam.turnon,
                "00:20.400": self.car.turnsignalson,
                "00:20.800": self.car.highbeam.turnon,
                "00:21.400": [
                    self.car.lowbeam.turnoff,
                    self.car.turnsignalsoff,
                    self.car.highbeam.turnoff,
                ],
                # (I aint got nothing to) Lose lose lose
                "00:23.500": self.car.lowbeam.turnon,
                "00:24.100": self.car.turnsignalson,
                "00:24.500": self.car.highbeam.turnon,
                "00:25.100": [
                    self.car.lowbeam.turnoff,
                    self.car.turnsignalsoff,
                    self.car.highbeam.turnoff,
                ],
                # I am going ha-a-ard
                "00:31.000": self.car.lowbeam.turnon,
                "00:31.600": self.car.turnsignalson,
                "00:32.000": self.car.highbeam.turnon,
                "00:32.600": self.car.parklight.turnon,
                "00:33.600": [
                    self.car.lowbeam.turnoff,
                    self.car.turnsignalsoff,
                    self.car.highbeam.turnoff,
                    self.car.parklight.turnoff,
                ],
                # oh yeah i am going i-i-in
                "00:35.000": self.car.lowbeam.turnon,
                "00:35.600": self.car.turnsignalson,
                "00:36.000": self.car.highbeam.turnon,
                "00:36.600": self.car.parklight.turnon,
                "00:37.600": [
                    self.car.lowbeam.turnoff,
                    self.car.turnsignalsoff,
                    self.car.highbeam.turnoff,
                    self.car.parklight.turnoff,
                ],
                # Let the party begi-i-i-in
                "00:38.700": self.car.lowbeam.turnon,
                "00:39.300": self.car.turnsignalson,
                "00:39.700": self.car.highbeam.turnon,
                "00:40.300": self.car.parklight.turnon,
                "00:41.300": [
                    self.car.lowbeam.turnoff,
                    self.car.turnsignalsoff,
                    self.car.highbeam.turnoff,
                    self.car.parklight.turnoff,
                ],
            },
            self.timeseries(  # Turn all the lights on!
                "00:46.250",
                duration_on=pd.Timedelta(milliseconds=250),
                interval=pd.Timedelta(milliseconds=450),
                periods=6,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(  # ooaah
                "00:50.000",
                duration_on=pd.Timedelta(milliseconds=250),
                interval=pd.Timedelta(milliseconds=450),
                periods=6,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(  # Turn all the lights on!
                "00:53.600",
                duration_on=pd.Timedelta(milliseconds=250),
                interval=pd.Timedelta(milliseconds=450),
                periods=6,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            self.timeseries(  # ah ha!
                "00:57.250",
                duration_on=pd.Timedelta(milliseconds=250),
                interval=pd.Timedelta(milliseconds=450),
                periods=2,
                action_on=self.car.turnallthelightson,
                action_off=self.car.turnallthelightsoff,
            ),
            {
                "01:01.500": self.car.highbeam.turnon,  # puts your hand if youre going haaaard
                "01:03.750": self.car.highbeam.turnoff,
                "01:05.350": self.car.highbeam.turnon,  # i need some light its way too dark
                "01:07.500": self.car.highbeam.turnoff,
                "01:09.000": self.car.highbeam.turnon,  # okay im going i-i-n
                "01:11.250": self.car.highbeam.turnoff,
                "01:15.500": self.car.turnallthelightson,  # TURN ALL THE LIGHTS ON
                "01:16.500": self.car.turnallthelightsoff,
            },
        ]
        return actions
