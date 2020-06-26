#!/usr/bin/env python3
import os
import sys
import psycopg2


def get_env(key: str):
    env = os.environ.get(key)
    if(env is None):
        raise Exception("Environment variable: " + key + " expected but not set!")
    return env


class Pass:
    def __init__(self, latitude, longitude, start, end, altitude, azimuth):
        pass


class DartDB:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.session = psycopg2.connect(database=database,
                                        user=user,
                                        password=password,
                                        host=host)
        self.cursor = self.session.cursor()
        self.schema = ['requests', 'passes', 'tles']

        for table in self.schema:
            if(not self.has_table(table)):
                raise psycopg2.DatabaseError(database
                                             + ' does not contain table: '
                                             + table)

    def add_request(self, user_id, orbital_pass):
        raise NotImplemented()
        # self.cursor.execute('INSERT INTO '
        #                     + self.schema[0]
        #                     + ' (added, header, first, second) \
        #                         VALUES (%(added)s, \
        #                                 %(header)s, \
        #                                 %(first)s, \
        #                                 %(second)s)',
        #                     {'user_id': user_id, 'latitude': latitude})
        # self.session.commit()

    def get_requests(self):
        self.cursor.execute('SELECT * FROM ' + self.schema[0] + ';')
        return list(map(lambda x: x[0], self.cursor.fetchall()))

    def add_tle(self, added: str, header: str, first: str, second: str):
        self.cursor.execute('INSERT INTO '
                            + self.schema[2]
                            + ' (added, header, first, second) \
                                VALUES (%(added)s, \
                                        %(header)s, \
                                        %(first)s, \
                                        %(second)s)',
                            {'added': added, 'header': header,
                             'first': first, 'second': second})
        # self.session.commit()

    def get_tles(self):
        self.cursor.execute('SELECT * FROM ' + self.schema[2] + ';')
        return self.cursor.fetchall()

    def close(self):
        self.session.commit()
        self.session.close()

    def has_table(self, table_name: str):
        schema = 'public'
        self.cursor.execute('SELECT EXISTS \
                                (SELECT FROM information_schema.tables \
                                 WHERE table_schema=%(schema)s \
                                 AND table_name=%(name)s);',
                            {'schema': schema, 'name': table_name})
        return self.cursor.fetchone()[0]

    def __str__(self):
        return str(self.session)


def main(args):
    host = get_env('DART_HOST')
    prod_path = get_env('DART_DB')
    username = get_env('DART_USERNAME')
    password = get_env('DART_PASSWORD')

    try:
        prod_db = DartDB(host, prod_path, username, password)

        if(len(args) == 4):
            prod_db.add_tle(args[0], args[1], args[2], args[3])

        tles = prod_db.get_tles()
        print('TLEs:')
        for tle in tles:
            print('\t' + str(tle))

    except psycopg2.DatabaseError as e:
        print(str(e))
        prod_db = None
    finally:
        if(prod_db is not None):
            prod_db.close()


if __name__ == "__main__":
    main(sys.argv[1:])
