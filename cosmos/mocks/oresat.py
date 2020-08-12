#!/usr/bin/env python3
import sys
import enum
import time
import socket
import argparse
import threading


class Mode(enum.Enum):
    info = 0
    warn = 1
    error = 2
    debug = 3

    def __repr__(self):
        return self.name.upper()


class MockOresat(threading.Thread):
    """
    Operates as a killable helper-thread for accepting connections from COSMOS
    """

    def __init__(self,
                 screen_lock: threading.Lock,
                 connection: socket.socket,
                 client: tuple,
                 *kwargs):
        super().__init__(target=self.event_loop)
        self.screen_lock = screen_lock
        self.connection = connection
        self.client = client
        self.setDaemon(True)
        self.name = 'Oresat Connection Listener{}'.format(self.client)
        self.alive = True

    def safe_print(self, msg: str, mode: Mode = Mode.info) -> None:
        thread_id = threading.get_ident()
        self.screen_lock.acquire()
        print('({})[{}][{}]: {}'.format(thread_id,
                                        time.ctime(),
                                        mode,
                                        msg))
        self.screen_lock.release()

    def extract_packet(self) -> int:
        cmd_data = self.connection.recv(256)
        if not cmd_data:
            raise Exception("Connection closed")

        print(cmd_data)  # pktid is the first 16 bytes
        pktid = cmd_data[:16]
        if pktid == 10:
            print("Received PASS_SCHEDULE command")
        elif pktid == 20:
            print("Received PASS_CANCEL command")
        else:
            e = "WHOA unexcepted pktid {} for command {}" \
                .format(pktid, cmd_data)
            raise Exception(e)
        return pktid

    def event_loop(self):
        self.safe_print('Accepted a new connection from {}'
                        .format(self.client))
        try:
            while self.alive:
                packet_id = self.extract_packet()
                self.safe_print('Recieved packet with id: {}'
                                .format(packet_id))
        except (KeyboardInterrupt, SystemExit):
            self.safe_print('Connection closed by server!')
        except Exception:
            self.safe_print('Connection closed by client!')
        finally:
            self.stop()

    def stop(self):
        if(not self.alive):
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
        else:
            self.safe_print('Listner with pid: {} was already closed!'
                            .format(self.ident))
        self.alive = False

    def __repr__(self):
        return '<MockOresat ({}) {} ({})>'.format(self.ident,
                                                  self.client,
                                                  self.connection)


def main(args):
    parser = argparse.ArgumentParser(prog='oresat',
                                     description='A mock of Oresat.',
                                     allow_abbrev=False)
    parser.add_argument('-H', '--host',
                        dest='host',
                        type=str,
                        nargs=1,
                        default='localhost',
                        help='[Default: localhost] Host for Mock Oresat to bind to.')
    parser.add_argument('-P', '--port',
                        dest='port',
                        type=int,
                        nargs=1,
                        default=8888,
                        help='[Default: 8888]: Port for Mock Oresat to bind to.')
    parser.add_argument('-m', '--max-connections',
                        dest='max_connections',
                        type=int,
                        nargs=1,
                        help='Maximum number of connections to accept.')
    args = parser.parse_args(args)
    screen_lock = threading.Lock()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.host, args.port))
    sock.listen(1)

    print('Opended OreSat Mock at {}:{}'.format(args.host,
                                                args.port))
    connections = []

    while True:
        try:
            connection, client = sock.accept()
            thread_count = len(threading.enumerate()) - 1

            if(args.max_connections is not None
                and thread_count >= args.max_connections[0]):
                print('Max connection limit reached! Throwing out connection!')
                connection.shutdown(socket.SHUT_RDWR)
                connection.close()
            else:
                new_connection = MockOresat(screen_lock, connection, client)
                connections.append(new_connection)
                new_connection.run()
        except (KeyboardInterrupt, SystemExit):
            for connection in connections:
                print('Closing connection: {}'.format(connection))
                connection.stop()
            sock.shutdown(socket.SHUT_RDWR)
            sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
