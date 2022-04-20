#!/usr/bin/env python3

import psycopg2
from time import sleep


while True:
    try:
        with psycopg2.connect(host='sql', user='app', dbname='ogle') as con:
            with con.cursor() as cur:
                cur.execute('SELECT * FROM catalog LIMIT 0')
        break
    except psycopg2.OperationalError:
        sleep(1)

print('POSTGRES IS AVAILABLE')
