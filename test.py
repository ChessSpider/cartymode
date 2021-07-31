import pandas as pd


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

        periods[period_on.strftime("%M:%S.%l")] = "action_on"
        periods[period_off.strftime("%M:%S.%l")] = "action_off"

    return periods


timeseries("00:01.100", duration_on="200ms", interval="400ms", periods=3)