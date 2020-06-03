from skyfield.api import Topos, load, EarthSatellite


class Event(object):
    """
    POD class for holding all info realated to a OreSat pass.
    """
    def __init__(self):
        # Datetime at Acquisition of Signal in UTC
        self.AOS_datetime = None
        # Datetime at Loss of Signal in UTC
        self.LOS_datetime = None
        # Total time of pass
        self.total_time = None
        # Azimuth at Acquistion of Signal
        self.AOS_azimuth = None
        # Azimuth at Loss of Signal
        self.LOS_azimuth = None
        # Altitude at Acquistion of Signal
        self.AOS_altitude = None
        # Altitude at Loss of Signal
        self.LOS_altitude = None


def get_events(satellite=None, gs_loc=None, t0=None, t1=None, deg=0.0):
    events_list = []

    t, events = satellite.find_events(gs_loc, t0, t1, deg)

    for ti, event in zip(t, events):
        name = ("above", "culminate", "below")[event]
        if event == 0: # above degrees
            new_event = Event()  # make event
            new_event.AOS_datetime = ti.utc_datetime()
        elif event == 2: # below degrees
            new_event.LOS_datetime = ti.utc_datetime()
            new_event.total_time = new_event.LOS_datetime - new_event.AOS_datetime
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
        print("Pass at: {datetime:%Y-%m-%d %H:%M:%S} for {duration:4.1f} minutes".format(datetime=e.AOS_datetime, duration=e.total_time.total_seconds()/60))

