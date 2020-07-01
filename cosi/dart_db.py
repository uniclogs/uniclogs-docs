import psycopg2


class DartDB:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.session = psycopg2.connect(database=database,
                                        user=user,
                                        password=password,
                                        host=host)
        self.cursor = self.session.cursor()
        self.schema = ['pass', 'requests', 'pass_requests', 'tles']

        for table in self.schema:
            if(not self.has_table(table)):
                path = 'cosi/schemas/' + table + '.sql'
                print(table + ' table not in ' + database + '!\n\tGenerating from file: ' + path)
                self.cursor.execute(open(path, 'r').read())
        self.session.commit()

    def add_request(self, user_id: str, orbital_pass: object):
        raise NotImplementedError()
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
