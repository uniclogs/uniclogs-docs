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
    2. ./send_test_csd.py

    You should see command show up in COSMOS!
"""

from ballcosmos.script import set_replay_mode, connect_interface, csd, shutdown_csd_tlm

set_replay_mode(False)
connect_interface('ENGR_LINK_INT')
print('sending command...')
csd("ENGR_LINK", "PASS_SCHEDULE", {"PKT_ID": 10, "PASS_ID": 100})
csd("ENGR_LINK", "PASS_CANCEL", {"PKT_ID": 20, "PASS_ID": 100})
print('command sent')
shutdown_csd_tlm()
