import sys
import random
import string
import getopt
sys.path.insert(0, '..')
from models import Request, Pass, Tle, Session, PassRequest
from datetime import datetime, timezone, timedelta
sys.path.insert(0, '../..')
import pass_calculator.calculator as pc


tle = [
    "1 25544U 98067A   20185.75040611  .00000600  00000-0  18779-4 0  9992",
    "2 25544  51.6453 266.4797 0002530 107.7809  36.4383 15.49478723234588"
    ]

# oregon as a box
MinLongitude = -116.926326
MaxLatitude = 46.211947
MaxLongitude = -124.001521
MinLatitude = 41.990853


days_in_past = 2
start = datetime.now()
start = start - timedelta(days=days_in_past)
start = start.replace(tzinfo=timezone.utc)


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generated_passes(num: int):
    generated_passes = []

    for i in range(num):
        days = random.randrange(days_in_past+7)
        start_day = start + timedelta(days=days)
        start_day = start_day.replace(tzinfo=timezone.utc)
        end_day = start_day + timedelta(days=1)
        end_day = end_day.replace(tzinfo=timezone.utc)

        latitude = round(random.uniform(MinLatitude, MaxLatitude), 6)
        longitude = round(random.uniform(MinLongitude, MaxLongitude), 6)
        elevation_m = round(random.uniform(0.0, 2000.0), 2)

        # call pass calculator
        orbital_passes = pc.get_all_passes(
                tle=tle,
                lat_deg=latitude,
                long_deg=longitude,
                start_datetime_utc=start_day,
                end_datetime_utc=end_day,
                elev_m=elevation_m
                )

        index = random.randrange(len(orbital_passes))
        generated_passes.append(orbital_passes[index])

    return generated_passes


def insert_into_db(generated_passes, random_status=False):
    session = Session()

    for p in generated_passes:

        # look for pass in db
        result = session.query(Pass)\
            .filter(Pass.start_time == p.aos_utc,
                    Pass.latitude == p.gs_latitude_deg,
                    Pass.longtitude == p.gs_longitude_deg)\
            .first()

        if result is None:
            # pass not in db, add it
            new_pass = Pass(
                latitude=p.gs_latitude_deg,
                longtitude=p.gs_longitude_deg,
                elevation=p.gs_elevation_m,
                start_time=p.aos_utc,
                end_time=p.los_utc
                )

            session.add(new_pass)
            session.flush()

            pass_uid = new_pass.uid
        else:
            # pass already in db
            pass_uid = result.uid

        # random statuses
        if random_status is True:
            approved_status = random.choice([True, False, None])
            sent_status = random.choice([True, False])
        else:
            approved_status = None
            sent_status = False

        # make a random created_dt
        days = random.randrange(14)
        mins = random.randrange(60)
        secs = random.randrange(60)
        created_dt = start - timedelta(days=days, minutes=mins, seconds=secs)
        created_dt = created_dt.replace(tzinfo=timezone.utc)

        new_request = Request(
            user_token=randomword(10),
            is_approved=approved_status,
            is_sent=sent_status,
            pass_uid=pass_uid,
            observation_type=random.choice(["cfc", "oresat live", "uniclogs"]),
            created_date=created_dt
            )

        session.add(new_request)
        session.flush()

        new_pass_request = PassRequest(
                pass_id=pass_uid,
                req_token=new_request.user_token
                )

        session.add(new_pass_request)
        session.flush()

    session.commit()
    session.close()


def clear_db():
    session = Session()

    result = session.query(PassRequest).all()

    for r in result:
        session.delete(r)

    result = session.query(Request).all()

    for r in result:
        session.delete(r)

    result = session.query(Pass).all()

    for r in result:
        session.delete(r)

    session.commit()
    session.close()


if __name__ == '__main__':
    num = 100
    random_status = False

    opts, argv = getopt.getopt(sys.argv[1:], "hcrn:")
    for o, a in opts:
        if o == '-h':
            print("""
            Flags
            -h   : help message
            -r   : randomize is_approved and is_sent statuses
            -n x : generate x passes where x > 0 and x < 10000
            -c   : clean db
            None : gererate 100 non randomize requests
            """)
            exit(0)
        elif o == '-c':
            clear_db()
            exit(0)
        elif o == '-r':
            random_status = True
        elif o == '-n':
            v = int(a)
            if v < 0 or v >= 10000:
                print("Can't be negative or greater than 10000")
                exit(0)
            num = v
        else:
            print("Unkown flag, run with -h for help message")
            exit(1)

    pass_list = generated_passes(num)
    insert_into_db(pass_list, random_status)
