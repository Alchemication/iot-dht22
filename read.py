#!/usr/bin/python3
import sqlite3
import json

print('[INFO] Reading config file...')
with open('./config.json') as config_file:
    cfg = json.load(config_file)

print('[INFO] Connecting to DB...')
conn = sqlite3.connect(cfg['dbFileName'])

print('[INFO] Reading from DB...')
cur = conn.cursor()
res = conn.execute("SELECT * FROM measurements LIMIT 100")

for r in res:
    print(r)

conn.commit()
conn.close()
print('[INFO] DONE')
    