#!/usr/bin/python3
"""Print parsed C3 beacon from SCS"""

import kiss
import time
from subprocess import Popen
import subprocess
import sys
import threading
import logging
import beacon
import bitstring
from datetime import datetime

# start the rtl_fm and direwolf commands
rtl_fm_args = ["rtl_fm", "-Mfm", "-f436.5M", "-p48.1", "-s96000", "-g30", "-"]
direwolf_args = ["direwolf", "-t0", "-r96000", "-D1", "-B9600", "-"]
rtl_fm_cmd = Popen(rtl_fm_args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
direwolf_cmd = Popen(direwolf_args, stdin=rtl_fm_cmd.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def parse_packet(x):
    # get the TNC command. We only support 0x00 data from
    cmd = x[0]
    if cmd != 0:
        logging.error("unknown command: " + str(cmd))
        return

    # decode the 14 byte address fields with the callsigned and SSIDs. The 
    # field is encoded shifted 1 but to the left, so shift it it to the right>
    addr = x[1:15]
    addr = (bitstring.BitArray(addr) >> 1).bytes
    to_cs = addr[0:6].decode('utf-8').strip() # To Callsign bytes 0-5
    to_ssid = addr[6:7].decode('utf-8') # To SSID byte 6
    from_cs = addr[7:13].decode('utf-8').strip() # From Callsign bytes 7-12
    from_ssid = addr[13:14].decode('utf-8') # From SSID byte 13

    # extract the the control and PID bytes
    ctrl = x[15:16]
    pid = x[16:17]

    # print the formatted packet header
    print("{}; FROM: {}[{}] ; TO: {}[{}] ; CTRL: 0x{} ; PID: 0x{}".format(
        datetime.now().isoformat(), from_cs, from_ssid, to_cs, to_ssid, ctrl.hex(), pid.hex()))

    # the rest of the frame is the payload
    payload = x[17:]
    beacon.dump(payload)

def read_kiss_forever():
    # wait just a sec for the rtl_fm and direwolf to start
    time.sleep(0.5)
    k = kiss.TCPKISS("localhost", 8001)
    k.start()  # start the TCP TNC connection
    k.read(callback=parse_packet) # set the TNC read callback

try:
    read_kiss_forever()
except KeyboardInterrupt:
    print("killing rtl_fm and direwolf...")
    rtl_fm_cmd.terminate()
    direwolf_cmd.terminate()
    sys.exit()
