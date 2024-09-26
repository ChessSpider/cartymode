from pandas._libs.tslibs.timestamps import Timestamp
from . import TimedAction, Song
import pandas as pd

import pandas as pd

class continuous(Song):
    spotify_id = "spotify:track:6LOOqW1iQwYNWF0Gtilu7H"
    car = None

    def __init__(self, car):
        super().__init__()
        self.car = car

    def format_timedelta(self, timedelta):
        """
        Format pd.Timedelta to '%M:%S.%f' (minutes:seconds.milliseconds) for the timeseries function.
        """
        total_seconds = int(timedelta.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        milliseconds = int(timedelta.microseconds / 1000)
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

    def return_actions(self):
        actions = []
        total_duration = pd.Timedelta(minutes=30)  # Total duration of 30 minutes
        interval = pd.Timedelta(seconds=10)        # Interval between actions
        lights = [
            ('lowbeam', self.car.lowbeam.turnon, self.car.lowbeam.turnoff),
            ('highbeam', self.car.highbeam.turnon, self.car.highbeam.turnoff),
            ('turnsignals', self.car.turnsignalson, self.car.turnsignalsoff),
            ('foglights', self.car.frontfog.turnon, self.car.frontfog.turnoff),
        ]
        
        num_lights = len(lights)
        cycle_duration = (num_lights + 1) * interval  # Dynamic cycle duration
        num_cycles = int(total_duration / cycle_duration)

        for cycle in range(num_cycles):
            cycle_start = pd.Timedelta(seconds=cycle * cycle_duration.total_seconds())
            
            # Turn on each light in sequence every 'interval' seconds
            for i, (light_name, light_on, light_off) in enumerate(lights):
                turn_on_time = cycle_start + i * interval
                formatted_turn_on_time = self.format_timedelta(turn_on_time)
                actions.append({formatted_turn_on_time: light_on})
            
            # After all lights are on, they stay on for 'interval' seconds
            # Then, turn off all lights simultaneously
            turn_off_time = cycle_start + num_lights * interval
            formatted_turn_off_time = self.format_timedelta(turn_off_time)
            for _, _, light_off in lights:
                actions.append({formatted_turn_off_time: light_off})
            
            # All lights remain off for 'interval' seconds before the next cycle starts

        return actions

