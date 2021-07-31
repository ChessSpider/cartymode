from . import TimedAction, Song


class caramelldansen(Song):
    spotify_id = "spotify:track:7MwwPyZJ7UKFROj2oVnH6R"
    car = None

    def __init__(self, car):
        self.car = car

    def return_actions(self):
        actions = [
            {
                "00:00.000": self.car.turnallthelightson,
                "00:14.000": self.car.turnallthelightsoff,
                "00:16.706": self.car.highbeam.turnon,
                "00:17.006": self.car.highbeam.turnoff,
                "00:18.125": self.car.highbeam.turnon,
                "00:18.425": self.car.highbeam.turnoff,
                "00:19.598": self.car.highbeam.turnon,
                "00:19.998": self.car.highbeam.turnoff,
                "00:20.980": self.car.highbeam.turnon,
                "00:21.298": self.car.highbeam.turnoff,
                "00:22.522": self.car.highbeam.turnon,
                "00:22.822": self.car.highbeam.turnoff,
                "00:23.895": self.car.highbeam.turnon,
                "00:24.100": self.car.highbeam.turnoff,
                "00:25.415": self.car.highbeam.turnon,
                "00:25.700": self.car.highbeam.turnoff,
                "00:26.850": self.car.highbeam.turnon,
                "00:27.100": self.car.highbeam.turnoff,
            },
            self.timeseries(
                "00:31.100",
                duration_on="100ms",
                interval="300ms",
                periods=20,
                action_on=self.car.highbeam.turnon,
                action_off=self.car.highbeam.turnoff,
            ),
        ]
        return actions
