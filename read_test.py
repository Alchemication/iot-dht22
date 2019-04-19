#!/usr/bin/python3
import sqlite3
import json
from probe import read_config

cfg = read_config()

print('[INFO] Connecting to DB...')
conn = sqlite3.connect(cfg['dbFileName'])

print('[INFO] Reading from DB...')
cur = conn.cursor()
res = conn.execute("SELECT * FROM measurements LIMIT 100")

for r in res:
    print(r)

conn.commit()
conn.close()
