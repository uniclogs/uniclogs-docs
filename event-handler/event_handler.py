import numpy as np
from beyond.io.tle import Tle
from beyond.frames import create_station
from beyond.dates import Date, timedelta


tle = Tle("""ISS (ZARYA)
1 25544U 98067A   20147.68235988  .00000878  00000-0  23780-4 0  9990
2 25544  51.6443  94.9049 0001567 359.6611  61.5558 15.49392416228680
""")


class Event(object):
    def __init__(self):
        self.AOS_time = Date.now()
        self.Max_time = Date.now()
        self.LOS_time = Date.now()
        self.total_event_time = timedelta(0)

    def __str__(self):
        return "Event at: {date:%Y-%m-%d %H:%M:%S}, for {duration:4.1f} minutes".format(date=self.AOS_time, duration=self.total_event_time.seconds/60)


def find_events(TLE, station, start_time, stop_time, mimium_event_time):
    events = []
    events_size = 0
    current_event = 0
    event_happening = False

    for orb in station.visibility(tle.orbit(), start=start_time, stop=stop_time, step=timedelta(minutes=1), events=True):

        if not orb.event:
            continue

        if orb.event.info == "AOS":
            event_happening = True
            new_event = Event()
            new_event.AOS_time = orb.date

        elif orb.event.info == "MAX":
            new_event.Max_time = orb.date

        elif orb.event.info == "LOS":
            event_happening = False
            new_event.LOS_time = orb.date
            new_event.total_event_time = new_event.LOS_time - new_event.AOS_time

            # append event to list if meet minium time
            if new_event.total_event_time > mimium_event_time:
                events.append(new_event)

    return events


if __name__ == "__main__":
    # Create a station for PSU
    station = create_station('PSU', (45.512778, -122.685278, 47.0)) # lat long elev(m)

    # find events for station
    events = find_events(tle, station, Date.now(), timedelta(days=5), timedelta(seconds=30))

    for i in events:
        print(i)
