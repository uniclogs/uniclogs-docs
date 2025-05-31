#!/usr/bin/env python3

import socket
import datetime


TEMP_APID = 1
TEMP_LEN = 18   # 14 bytes of header + 4 of payload
LOG_APID = 3
LOG_LEN = 94    # 14 bytes of header + 80 of payload


def print_packet(payload):
    print("total len: ", len(payload))
    for char in payload:
        print(hex(char), end=" ")
    print()


def get_primary_header(apid, packet_len):
    if packet_len > 256:
        raise Exception("TODO support using second byte for packet length!")

    # PRIMARY HEADER
    rv = [
        8,              # first byte is always 8 if CCSDS SECONDARY HEADER (5th bit == 1, rest are 0)
        apid,           # CCSDS APP PROCESS ID
        0, 0,           # sequence count/name (unused)
        0, packet_len   # CCSDS TOTAL PACKET DATA LENGTH
    ]
    return rv


def get_secondary_header():
    # just do arbitrary offset to emphasize this isn't the present, but historical data
    now = datetime.datetime.now() - datetime.timedelta(days=1, hours=17)
    rv = [0x07, 0xe4]           # 2020 in hex
    rv.append(now.month)
    rv.append(now.day)
    rv.append(now.hour)
    rv.append(now.minute)
    rv.append(now.second)
    rv.append(0)                # spacer
    return rv


def send_spp_temp(connection, temp1, temp2):
    payload = get_primary_header(TEMP_APID, TEMP_LEN)
    payload += get_secondary_header()

    payload.append(0)
    payload.append(temp1)
    payload.append(0)
    payload.append(temp2)

    # print_packet(payload)
    if connection:
        connection.send(bytes(payload))


def send_spp_log(connection, log):
    header = get_primary_header(LOG_APID, LOG_LEN)
    header += get_secondary_header()

    payload = header + list(log.encode('ascii'))
    while len(payload) < LOG_LEN:
        payload.append(0)

    # print_packet(payload)
    if connection:
        connection.send(bytes(payload))


def receive_packet(connection):
    csd_data = connection.recv(256)
    if not csd_data:
        raise Exception("Connection closed")

    pktid = bytearray(csd_data)[7]  # pktid is the 8th byte
    if pktid == 1:
        print("received COLLECT command")
    elif pktid == 2:
        print("received ABORT command")
    else:
        e = "WHOA unexcepted pktid {} for command {}".format(pktid, csd_data)
        raise Exception(e)
    return pktid


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8888)
    sock.bind(server_address)
    sock.listen(1)

    print('waiting for a connection on %s port %s' % server_address)
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)
        while True:
            pktid = receive_packet(connection)

            if pktid == 1:
                print('sending temperature log')
                send_spp_log(connection, "plz help on fire")
                print('sending temperature telemetry')
                send_spp_temp(connection, 100, 102)
            elif pktid == 2:
                print("TODO")
    except KeyboardInterrupt:
        print('Goodbye')
    finally:
        print('shutting down socket')
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
