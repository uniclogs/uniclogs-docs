#!/usr/bin/python3
"""Print parsed C3 beacon from SCS"""

import sys
from serial import Serial, SerialException
import beacon
from datetime import datetime

def _readline(ser):
    eol = b'\r\n'
    leneol = len(eol)
    line = bytearray()
    while True:
        c = ser.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)

def main():
    # open serial
    tty = '/dev/serial/by-id/usb-SCS_SCS_Tracker___DSP_TNC_PT2HJ743-if00-port0'
    ser = Serial(tty, 38400, timeout=15.0)

    while 1:
        try:
            line = _readline(ser)
        except SerialException as exc:
            print('Device error: {}\n'.format(exc))
            break

        # filter out too short lines
        if len(line) < 3:
            continue

        # just print header lines and continue
        if 'KJ7SAT' in str(line):
            print("{}; {}".format(datetime.now().isoformat(), line.decode('utf-8').strip()))
            continue

        # strip the carriage return and newline.
        line = line[:len(line)-2]

        beacon.dump(line)
        print("")
    
try:
    main()
except KeyboardInterrupt:
    sys.exit()
