## connect to the Space-Track.org API
## spaceTrack.py
## need space-track.org un/pw credentials and norad_id for satellite

import requests
import json
import sys
from common import  URl_BASE, \
                    REQUEST_LOGIN, \
                    REQUEST_DETAILS
from utilities import dump_json

def credentials(usr, pwd):
    siteCred = {'identity': usr, 'password': pwd}
    return siteCred

class MyError(Exception):
    def __init___(self,args):
        super().__init__(self,"Exception raised with arguments {0}".format(args))
        self.args = args

# norad_id = 25544 for ISS (ZARYA)
def getTLE(siteCred, norad_id):
    data = []
    sat_id = norad_id
  
    with requests.Session() as session:
        resp = session.post(URL_BASE + REQUEST_LOGIN, data = siteCred)
        if resp.status_code != 200:
            raise MyError(resp, "Credentials fail on login")

        resp = session.get(URL_BASE + TLE_REQUESTER + str(sat_id) + REQUEST_DETAILS)
        if resp.status_code != 200:
            print(resp)
            raise MyError(resp, "TLE request fails, check credentials")


        # output to file in json format
        data = json.loads(resp.text)
        outfile = open('jsonOutput.json', 'w')
        dump_json(outfile, data)

        # or just return data from function
        print("process complete")
    return data


if __name__ == "__main__":
    siteCred = credentials(usr, pwd)
    tleOutput = getTLE(siteCred, norad_id)
