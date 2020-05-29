from skyfield.api import Topos, load, EarthSatellite

class Event(object):
    def __init__(self):
        self.AOS_time = None
        self.LOS_time = None
        self.total_time = None

def get_events(satellite=None, gs_loc=None, t0=None, t1=None, deg=0.0):
    events_list = []

    t, events = satellite.find_events(gs_loc, t0, t1, deg)

    for ti, event in zip(t, events):
        name = ("above", "culminate", "below")[event]
        if event == 0: # above degrees
            new_event = Event()  # make event
            new_event.AOS_time = ti.utc_datetime()
        elif event == 2: # below degrees
            new_event.LOS_time = ti.utc_datetime()
            new_event.total_time = new_event.LOS_time - new_event.AOS_time
            events_list.append(new_event) # add event

    return events_list

if __name__ == "__main__":
    ts = load.timescale()
    line1 = "1 25544U 98067A   20147.68235988  .00000878  00000-0  23780-4 0  9990"
    line2 = "2 25544  51.6443  94.9049 0001567 359.6611  61.5558 15.49392416228680"
    satellite = EarthSatellite(line1, line2, "ISS (ZARYA)", ts)

    gs_loc = Topos(latitude_degrees=45.512778, longitude_degrees=122.685278, elevation_m=47.0)
    t0 = ts.utc(2020, 5, 26)
    t1 = ts.utc(2020, 5, 29)

    events = get_events(satellite, gs_loc, t0, t1, 0.0)

    for e in events:
        print("Pass at: {date:%Y-%m-%d %H:%M:%S} for {duration:4.1f} minutes".format(date=e.AOS_time, duration=e.total_time.total_seconds()/60))

