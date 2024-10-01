#!/usr/bin/env python3

import logging
from time import sleep

import psycopg2


while True:
    try:
        with psycopg2.connect(host='sql', user='app', dbname='ogle') as con:
            with con.cursor() as cur:
                cur.execute('SELECT * FROM catalog LIMIT 0')
        break
    except (psycopg2.errors.UndefinedTable, psycopg2.OperationalError):
        logging.info('waiting postgres to have "catalog" table')
        sleep(1)

logging.warning('POSTGRES IS AVAILABLE')
