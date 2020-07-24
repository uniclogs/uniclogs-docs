#schedule_pass.py

import os 
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import psycopg2
import pandas as pd
from ballcosmos.script \
    import set_replay_mode,\
            connect_interface,\
            cmd, shutdown_cmd_tlm


# short example list for testing purposes   
# a <pass> consists of UID, latitude, longitude, start_time, end_time, elevation
#passRequestList = pd.read_csv('passData.csv', sep=',', header='infer')

class Schedule_Pass:
    def __init__(self):
        """
        Schedule_Pass data object is loaded with data 
        from Passes table retrieved through RADS

        Attributes
        ----------
        passRequestList : pandas dataframe of table data
            each row contains a 'pass' consisting of 
            Pass_ID, Latitude, Longitude, StartTime, EndTime
        numberOfRequests : number of passes to be scheduled or canceled
        """
        self.passRequestList = pd.read_csv('passData.csv', sep=',', header='infer', dtype=str)
        self.passRequestList = pd.DataFrame((self.passRequestList),\
                columns=['idx','pass_id','latitude','longitude','start_time','end_time','elevation'])
        #self.passRequestList = self.passRequestList.astype({\
        #    "idx":'int16', "pass_id":'string',\
        #    "latitude":'string', "longitude":'string',\
        #    "start_time":'string',"end_time":'string',\
        #   "elevation":'string'})
        self.numberOfRequests =  len(self.passRequestList.index)


    def show_list(self):
        """ Prints pass_id for items on current list 
            for user confirmation of items on the list.

        Attributes
        ----------
        None. 
        """
        return print("Current list: \n{}\n".format(self.passRequestList))


    def sched(self, pass_info, index):
        """ Helper function to send attribute info to Cosmos interface
            to schedule passes. Called by schedule_all().
        """

        set_replay_mode(False)
        connect_interface('ENGR_LINK_INT')
        print('\nsending SCHEDULE command for PASS_ID: {}...\n'\
                .format(pass_info.loc[index, 'pass_id']))
        cmd("ENGR_LINK", "PASS_SCHEDULE",\
            {"PKT_ID": 10,\
             "PASS_ID": pass_info.loc[index,'pass_id'],\
             "LATITUDE": pass_info.loc[index, 'latitude'],\
             "LONGITUDE": pass_info.loc[index, 'longitude'],\
             "AOS": pass_info.loc[index, 'start_time'],\
             })
        shutdown_cmd_tlm()

        return print('command sent')


    def cancel(self, pass_info, index):
        """ Helper function to send attribute info to Cosmos interface
            to schedule passes. Called by cancel_all().
        """
        set_replay_mode(False)
        connect_interface('ENGR_LINK_INT')
        print('\nsending CANCEL command...\n{}\n'\
                .format(pass_info.loc[index,'pass_id']))
        cmd("ENGR_LINK", "PASS_CANCEL",\
            {"PKT_ID": 20,\
             "PASS_ID": pass_info.loc[index,'pass_id'],\
            })
        shutdown_cmd_tlm()
        # need error check 
        # condition to show passes cancelled is True
        return print('command sent')


    def schedule_all(self):
        """ Iterates through list to send schedule pass requests message 
            for all passes on list

        Attributes
        ----------
        passRequestList : list retrieved from pass_request database
        numberOfRequests : total number of passes to schedule 

        """
        for row in range(0,self.numberOfRequests):
            self.sched(self.passRequestList,row)

        return print("\n{} requests(s) sent.".format(self.numberOfRequests))


    def cancel_all(self):
        """ Iterates through list to send ancels all pass requests staged in satellite

        Attributes
        ----------
        passRequestList : list retrieved from pass_request database
        elem : provides user feedback on number of approved requests
        response: collects user input
        emptyPassRequestList : collects the newly emptied list
        """
        print("This request cannot be undone.")
        response = input("y/n: ")
        if response.lower() == 'y' or response.lower() == 'yes':
            for row in range(0,self.numberOfRequests):
                self.cancel(self.passRequestList,row)
            return print("{} requests(s) deleted.".format(self.numberOfRequests))
        else:
            print("List not deleted")
            return self.passRequestList


#if __name__ == "__main__":
    #sp = Schedule_Pass()
    #sp.show_list()
    #sp.schedule_all()
    #sp.cancel_all()



"""
    set_replay_mode(False)
    connect_interface('ENGR_LINK_INT')
    print('sending command...')
    cmd("ENGR_LINK", "PASS_SCHEDULE", {"PKT_ID": 10, "PASS_ID": 100})
    cmd("ENGR_LINK", "PASS_CANCEL", {"PKT_ID": 20, "PASS_ID": 100})
    print('command sent')
    shutdown_cmd_tlm()

"""
#!/usr/bin/env python3
"""
All paths relative from uniclogs-software git root directory
To run this script,
    Terminal 1:
    1. ./cosmos/mock_oresat/oresat_listen_for_commands.py
    Terminal 2:
    1. cd cosmos
    2. run `ruby Launcher`
    3. start COSMOS Command and Telemetry Server
    4. click "Connect" on ENGR_LINK_INT
    Now both COSMOS and Terminal 1 should indicate they are connected
    Terminal 3:
    1. cd cosi
    2. ./send_test_cmd.py
    You should see command show up in COSMOS!
"""


