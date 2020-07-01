#!/usr/bin/env python3
import os
import sys
import csv


def load_csv(path):
    res = []
    file = open(path, 'r', newline='')
    csvreader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
    for row in csvreader:
        res.append(row)
    file.close()
    return res


def main(args):
    if(len(args) == 0):
        print('Expected path to CSV.')
        sys.exit(-1)

    dart_host = os.getenv('DART_HOST')
    dart_db = os.getenv('DART_DB')
    dart_username = os.getenv('DART_USERNAME')
    dart_password = os.getenv('DART_PASSWORD')

    raw_requests = load_csv(args[0])
    print('raw requests: ' + str(raw_requests))


if __name__ == "__main__":
    main(sys.argv[1:])
