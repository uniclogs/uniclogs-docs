#!/usr/bin/env python3

import socket
import datetime


def receive_packet(connection):
    cmd_data = connection.recv(256)
    if not cmd_data:
        raise Exception("Connection closed")

    print(cmd_data)  # pktid is the first 16 bytes
    return
    if pktid == 10:
        print("received PASS_SCHEDULE command")
    elif pktid == 20:
        print("received PASS_CANCEL command")
    else:
        e = "WHOA unexcepted pktid {} for command {}".format(pktid, cmd_data)
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
    except KeyboardInterrupt:
        print('Goodbye')
    finally:
        print('shutting down socket')
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
