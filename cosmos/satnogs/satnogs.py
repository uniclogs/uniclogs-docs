#!/usr/bin/env python3
import sys
import common


def error(msg):
    print('fatal: ' + msg)
    sys.exit(-1)


def get_telemetry():
    pass


def main(args):
    print("args: " + str(args))
    print('Using token: ' + common.API_TOKEN)

    if(len(args) == 0):
        error('No CSIM Id specified!')


if __name__ == "__main__":
    main(sys.argv[1:])
