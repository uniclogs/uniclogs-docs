#!/usr/bin/env python3
import argparse

VALID_STR = 'L{} \'{}\' ... [VALID]'
INVALID_STR = 'L{} \'{}\' ... [INVALID] (expected: {}, got: {})'


def calculate_checksum(line: str) -> int:
    sum = 0
    for c in line[:-1]:
        if(c.isnumeric()):
            sum += int(c)
        elif(c == '-'):
            sum += 1
    return sum % 10


def main() -> None:
    parser = argparse.ArgumentParser(prog='tle-validate-checksum',
                                     description='A quick-n-dirty checksum'
                                     ' validator for two line elements',
                                     allow_abbrev=False)
    parser.add_argument('tle_file',
                        type=str,
                        help='path to a TLE file to validate')
    parser.add_argument('--quiet', '-q',
                        dest='keep_quiet',
                        action='store_true',
                        default=False,
                        help='only print output if there is an error')
    args = parser.parse_args()

    # Open the TLE file and read the lines
    with open(args.tle_file, 'r') as file:
        raw = file.read()

    # Calculate checksums for each line and print results to STDOUT
    lines = raw.split('\n')[:-1]
    if(len(lines) > 2):
        raise ValueError(f'File: {args.tle_file} is not a TLE!')

    for i, line in enumerate(lines):
        if(not line[-1].isdigit()):
            raise ValueError(f'File: {args.tle_file} is not a TLE!')
        actual = int(line[-1])
        checksum = calculate_checksum(line)
        is_valid = actual == checksum

        if(args.keep_quiet):
            if(not is_valid):
                print(INVALID_STR.format(i + 1, line, checksum, actual))
        else:
            if(is_valid):
                print(VALID_STR.format(i + 1, line))
            else:
                print(INVALID_STR.format(i + 1, line, checksum, actual))


if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)
