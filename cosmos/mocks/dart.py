#!/usr/bin/env python3
import sys
import socket


def recieve_cmd(connection):
    cmd_data = connection.recv(256)
    # if not cmd_data:
    #     raise ValueError('Connection closed by remote host!')

    packet_id = cmd_data[:16]
    print('Command: {}'.format(cmd_data))
    return packet_id


def main(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 7777)
    sock.bind(server_address)
    sock.listen(1)

    connection, client_address = sock.accept()

    while True:
        try:
            print('Recieved connection from: {}'.format(client_address))
            packet_id = recieve_cmd(connection)
            print('Packet ID: {}'.format(packet_id))
            connection.send(b'CMD OK\0')
        except KeyboardInterrupt:
            print('Recieved signal to stop mock DART!')
        finally:
            print('Closing server...')
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()


if __name__ == "__main__":
    main(sys.argv[1:])
