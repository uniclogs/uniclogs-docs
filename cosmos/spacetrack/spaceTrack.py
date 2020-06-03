## connect to the Space-Track.org API
## spaceTrack.py

## Code adapted from 
## (c) 2019 Andrew Stokes  All Rights Reserved
# See https://www.space-track.org/documentation

import requests
import json
import time
from datetime import datetime
import os, argparse

class MyError(Exception):
    def __init___(self,args):
        Exception.__init__(self,"my exception was raised with arguments {0}".format(args))
        self.args = args


uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"
requestCmdAction       = "/basicspacedata/query"
requestFindStarlinks   = "/class/tle/NORAD_CAT_ID/25544/orderby/EPOCH desc/limit/5/format/json"


""" for testing purposes here are space-track credentials"""
#configUsr = 'djernaes@pdx.edu'
#configPwd = 'NrXwf-mYc6Hx2cZ'


parser = argparse.ArgumentParser()
parser.add_argument("username", help="arg1 = username")
parser.add_argument("password", help="arg2 = password")
args = parser.parse_args()
configUsr = args.username
configPwd = args.password

siteCred = {'identity': configUsr, 'password': configPwd}


# use requests package to drive the RESTful session with space-track.org
with requests.Session() as session:
    # run the session in a with block to force session to close if we exit

    # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
    resp = session.post(uriBase + requestLogin, data = siteCred)
    if resp.status_code != 200:
        raise MyError(resp, "POST fail on login")

    # this query picks up all Starlink satellites from the catalog. Note - a 401 failure shows you have bad credentials 
    resp = session.get(uriBase + requestCmdAction + requestFindStarlinks)
    if resp.status_code != 200:
        print(resp)
        raise MyError(resp, "GET fail on request for Starlink satellites")

    # output to file in json format
    retData = json.loads(resp.text)
    with open('jsonOutput.txt', 'w') as outFile:
        json.dump(retData, outFile)


print("Completed session") 
