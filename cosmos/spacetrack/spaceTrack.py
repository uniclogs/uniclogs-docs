## connect to the Space-Track.org API
## spaceTrack.py
## need space-track.org un/pw credentials and norad_id for satellite

import requests
import json
import os, sys


def credentials(usr, pwd):
    siteCred = {'identity': usr, 'password': pwd}
    return siteCred

def get_Norad_id(norad_id):
    return norad_id

class MyError(Exception):
    def __init___(self,args):
        Exception.__init__(self,"Exception raised with arguments {0}".format(args))
        self.args = args

# norad_id = 25544 for ISS (ZARYA)
def getTLE(siteCred, norad_id):

    uriBase                = "https://www.space-track.org"
    requestLogin           = "/ajaxauth/login"
    requestTLE             = "/basicspacedata/query/class/tle/NORAD_CAT_ID/"
    sat_id                 = norad_id
    requestDetails         ="/predicates/TLE_LINE1,TLE_LINE2/limit/1/format/json"

    with requests.Session() as session:
        resp = session.post(uriBase + requestLogin, data = siteCred)
        if resp.status_code != 200:
            raise MyError(resp, "Credentials fail on login")

        resp = session.get(uriBase + requestTLE + str(norad_id) + requestDetails)
        if resp.status_code != 200:
            print(resp)
            raise MyError(resp, "TLE request fails, check credentials")


        # output to file in json format
        retData = json.loads(resp.text)
        with open('jsonOutput.json', 'w') as outFile:
            json.dump(retData, outFile)
        # or just return data from function    
        print("process complete")
    return retData


if __name__ == "__main__":
    siteCred = credentials(usr, pwd)
    norad_id = get_Norad_id(25544)
    tleOutput = getTLE(siteCred, norad_id)
