#!/usr/bin/python3
import sqlite3
import os
import sys
import json
from probe import read_config

def create_db(cfg):

    print('[INFO] Reading config file...')
    with open('./config.json') as config_file:
        cfg = json.load(config_file)

    print('[INFO] Checking if DB file already exists...')
    if os.path.isfile(cfg['dbFileName']):
        print('[ERROR] DB already created: {}'.format(cfg['dbFileName']))
        sys.exit(1)

    print('[INFO] Connecting to DB...')
    conn = sqlite3.connect(cfg['dbFileName'])

    #use following to create initial table
    print('[INFO] Creating DB...')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE measurements (
            id INTEGER PRIMARY KEY, 
            temp REAL, 
            hum REAL, 
            device TEXT, 
            [ts] timestamp
        )""")

    conn.commit()
    conn.close()
    print('[INFO] Done')
    sys.exit(0)

if __name__ == '__main__':
    cfg = read_config()
    create_db(cfg)