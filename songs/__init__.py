import datetime
import time
import threading
import pandas as pd
import logging

LOG = logging.getLogger(__name__)


class TimedAction(object):
    """
    A list of actions which has to happen at a certain time.
    Input: timestamp=HH:MM:SS, action= list of function-references to execute (e.g. turn light on, etc)
    """

    def __init__(self, timestamp, action):
        self.time = datetime.datetime.strptime(timestamp, "%M:%S.%f")
        self.actions = action if isinstance(action, list) else [action]

    def __sub__(self, other):
        return self.time - other.time

    def __lt__(self, other):
        return self.time < other.time

    def __add__(self, other: "TimedAction"):
        if self.time == other.time:
            self.actions = self.actions + other.actions
            return self
        else:
            raise Exception("Cannot add: Time index does not match")

    def __str__(self):

        return "{time}: {action}".format(
            time=self.time.strftime("%M:%S.%f"),
            action=", ".join(
                [
                    action.__self__.__class__.__name__ + "."
                    #   + action.__self__.lightstring
                    #   + "."
                    + action.__name__
                    for action in self.actions
                ]
            ),
        )

    def __call__(self):
        if len(self.actions) > 0:
            for action in self.actions:
                action()
            self.actions[
                0
            ].__self__.send()  # for can0/vcan0, this is needed to really send it
        else:
            raise Exception("No actions to call!")


class Song(object):
    spotify_id = ""
    car = None

    def timeseries(
        self,
        starttime="00:00.000",
        duration_on="300ms",
        interval="600ms",
        periods=3,
        action_on=None,
        action_off=None,
    ):
        starttime = pd.Timestamp("00:" + starttime)

        pr_on = pd.period_range(starttime, periods=periods, freq=interval)
        pr_off = pd.period_range(
            starttime + pd.Timedelta(duration_on), periods=periods, freq=interval
        )

        periods = {}
        for i in range(len(pr_on)):
            period_on = pr_on[i]
            period_off = pr_off[i]

            periods[period_on.strftime("%M:%S.%l")] = action_on
            periods[period_off.strftime("%M:%S.%l")] = action_off

        return periods

    def return_actions(self):
        return [{}]

    def get_timed_actions(self):
        ## Merge all the dictionaries into one dict
        actiondict = {}
        for action in self.return_actions():
            for timestamp, action in action.items():
                if timestamp not in actiondict:
                    actiondict[timestamp] = TimedAction(timestamp, action)
                else:
                    actiondict[timestamp] += TimedAction(timestamp, action)

        actionlist = []
        for timestamp, ta in actiondict.items():
            actionlist.append(ta)
        return sorted(actionlist)

    def play_sequence(self, offset="00:00.000"):
        actionlist = self.get_timed_actions()

        dt_offset = datetime.datetime.strptime(offset, "%M:%S.%f")
        skipped = False
        for i, ta in enumerate(actionlist):
            if ta.time < dt_offset:
                LOG.debug(f"Skipping {ta} because requested song offset = {offset}")
                skipped = True
                continue
            if skipped:
                # We skipped some TimedActions.. we have to sync
                sleepfor = ta - actionlist[i - 1]
                LOG.debug("SYNCING...Sleeping for %f" % sleepfor.total_seconds())
                time.sleep(sleepfor.total_seconds())
                skipped = False
                LOG.debug("SYNCED!")
            # print(ta)
            ta()
            try:
                sleepfor = actionlist[i + 1] - ta
                #    print("Sleeping for %f" % sleepfor.total_seconds())
                time.sleep(sleepfor.total_seconds())
            except IndexError:
                LOG.info("End of commands")

    def start(self, spotify, target_device, offset="00:00.000"):
        skip_ms = 0
        if offset != "00:00.000":
            # calculate millisecond offset for spotify
            minutes, seconds = offset.split(":")
            seconds, skip_ms = seconds.split(".")
            skip_ms = int(skip_ms)
            skip_ms += int(seconds) * 1000
            skip_ms += int(minutes) * 60 * 1000
            LOG.info(f"Skipping {skip_ms}ms ")

        th = threading.Thread(target=self.play_sequence, kwargs={"offset": offset})
        spotify.start_playback(
            uris=[self.spotify_id],
            device_id=target_device,
        )
        spotify.pause_playback()
        spotify.seek_track(skip_ms)
        LOG.info("Starting playback..")
        spotify.start_playback()
        th.start()
        return th
