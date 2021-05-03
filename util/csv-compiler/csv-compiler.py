#!/usr/bin/env python3
import csv
import yaml
import argparse

TYPES = {
    '': 'b1',
    'BOOL': 'b1',
    'INT8': 's1',
    'UINT8': 'u1',
    'State': 'b1',
    'INT16': 's2',
    'UINT16': 'u2',
    'INT24': 's3',
    'UINT24': 'u3',
    'INT32': 's4',
    'UINT32': 'u4',
    'INT64': 's8',
    'UINT64': 'u8',
}


def clean_name(name: str) -> str:
    return name.strip() \
             .lower() \
             .replace(' ', '_') \
             .replace('+', '_plus_') \
             .replace('-', '_minus_') \
             .replace('?', '')


def main():
    parser = argparse.ArgumentParser(prog='csv-compiler',
                                     description='A compiler to convert a CSV'
                                                 ' of APRS packet field to a'
                                                 ' target format.',
                                     allow_abbrev=False)
    parser.add_argument('--target', '-t',
                        dest='target',
                        type=str,
                        choices={'yml'},
                        default='yml',
                        help='the target format to convert to')
    parser.add_argument('csv_file',
                        help='The CSV file to compile')
    args = parser.parse_args()
    infile_name = args.csv_file
    infile_type = infile_name.split('.')[1]
    base_name = infile_name.split('.')[0]
    outfile_type = args.target
    outfile_name = f'{base_name}.{outfile_type}'

    if(infile_type != 'csv'):
        raise ValueError('File must be of type CSV!')

    with open(infile_name) as infile, \
         open(outfile_name, 'w+') as outfile:
        reader = csv.reader(infile)
        entries = []

        for i, line in enumerate(reader):
            system = clean_name(line[0])
            subsystem = clean_name(line[1])
            data = clean_name(line[2])

            varname = f'{system}_{subsystem}_{data}' \
                if(subsystem != '') else f'{system}_{data}'
            vartype = TYPES[line[3]]

            entry = {
                'id': varname,
                'type': vartype,
            }

            if(line[4] != ''):
                entry['doc'] = line[4]

            entries.append(entry)

        yaml.dump(entries, outfile, default_flow_style=False)


if __name__ == '__main__':
    main()
