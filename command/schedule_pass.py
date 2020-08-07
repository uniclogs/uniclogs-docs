#schedule_pass.py

import os 
import numpy as np
from ballcosmos.script \
    import set_replay_mode,\
            connect_interface,\
            cmd, shutdown_cmd_tlm


class Schedule_Pass:
    def __init__(self, request):
        """
        Schedule_Pass data object is loaded with data 
        from Passes table retrieved through RADS

        Attributes
        ----------
        passRequestList : a query/list received from RADS consisting of  
            request = (
                [0] user_token,
                [1] pass_uid,
                [2] is_approved,
                [3] is_sent,
                [4] created_date,
                [5] observation_type,
                [6] pass_data.latitude,
                [7] pass_data.longitude,
                [8] pass_data.elevation,
                [9] pass_data.start_time,
                [10] pass_data.end_time
                )

         
            Note: only the pass_uid, latitude, longitude, start_time will be 
            sent to the satellite
        numberOfRequests : number of passes to be scheduled or canceled
        """
        self.passRequestList = request
        self.numberOfRequests =  len(self.passRequestList)


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
                .format(pass_info[1]))

        # typecasts for cmd_tlm_server input
        pass_id = np.uint16(pass_info[1])
        latitude = np.float32(pass_info[6])
        longitude = np.float32(pass_info[7])
        AOS = str(pass_info[9])

        cmd("ENGR_LINK", "PASS_SCHEDULE",\
            {"PKT_ID": 10,\
             "PASS_ID": pass_id,\
             "LATITUDE": latitude,\
             "LONGITUDE": longitude,\
             "AOS": AOS })
        shutdown_cmd_tlm()

        return print('command sent')


    def cancel(self, pass_info, index):
        """ Helper function to send attribute info to Cosmos interface
            to schedule passes. Called by cancel_all().
        """
        set_replay_mode(False)
        connect_interface('ENGR_LINK_INT')
        print('\nsending CANCEL command...\n{}\n'\
                .format(pass_info[1]))
        # cast to uint16 for cmd_tlm_server
        pass_id = np.uint16(pass_info[1])
        cmd("ENGR_LINK", "PASS_CANCEL",\
            {"PKT_ID": 20,\
             "PASS_ID":pass_id })
        shutdown_cmd_tlm()

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
        """ Iterates through list to cancel all pass requests staged in satellite

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
    #sp = Schedule_Pass(request)
    #sp.show_list()
    #sp.schedule_all()
    #sp.cancel_all()



# for testing purposes: 
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
    2. ./schedule_pass.py
    You should see command show up in COSMOS!
"""


