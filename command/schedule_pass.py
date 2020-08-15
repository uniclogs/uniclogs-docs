#schedule_pass.py

import os 
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
                uid,
                user_token,
                pass_uid,
                is_approved,
                is_sent,
                created_date,
                updated_date,
                observation_type,
                pass_data.latitude,
                pass_data.longitude,
                pass_data.elevation,
                pass_data.start_time,
                pass_data.end_time
                )


            Note: only the pass_uid, latitude, longitude, start_time 
            will be sent to the satellite.
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


    def sched(self, pass_info):
        """ Helper function to send attribute info to Cosmos interface
            to schedule passes. Called by schedule_all().
        """
        print('\nsending SCHEDULE command for PASS_ID: {}...\n'\
                .format(pass_info.pass_id))

        pass_id = pass_info.pass_id
        latitude = pass_info.latitude
        longitude = pass_info.longitude
        AOS = pass_info.start_time

        cmd("ENGR_LINK PASS_SCHEDULE with PKT_ID 10, PASS_ID {}, LATITUDE {}, LONGITUDE {}, AOS {}"\
            .format(pass_id, latitude, longitude, AOS))

        return print('command sent')


    def cancel(self, pass_info):
        """ Helper function to send attribute info to Cosmos interface
            to schedule passes. Called by cancel_all().
        """

        print('\nsending CANCEL command for PASS_ID: {}...\n'\
            .format(pass_info.pass_id))
        cmd("ENGR_LINK PASS_CANCEL with PKT_ID 20, PASS_ID {}"\
            .format(pass_info.pass_id))

        return print('command sent')


    def schedule_all(self):
        """ Iterates through list to send schedule pass requests message 
            for all passes on list

        Attributes
        ----------
        passRequestList : list retrieved from pass_request database
        numberOfRequests : total number of passes to schedule 

        """
        set_replay_mode(False)
        connect_interface('ENGR_LINK_INT')

        for row in range(0,self.numberOfRequests):
            if self.passRequestList[row].is_approved is True:
                self.sched(self.passRequestList[row])

        shutdown_cmd_tlm()

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
        set_replay_mode(False)
        connect_interface('ENGR_LINK_INT')

        for row in range(0,self.numberOfRequests):
            if self.passRequestList[row].is_approved is False\
                and self.passRequestList[row].is_sent is True:
                self.cancel(self.passRequestList[row])

        shutdown_cmd_tlm()
        return print("{} requests(s) deleted.".format(self.numberOfRequests))


# for testing purposes: 
#if __name__ == "__main__":
    #sp = Schedule_Pass(request)
    #sp.show_list()
    #sp.schedule_all()
    #sp.cancel_all()



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


