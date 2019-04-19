#!/usr/bin/python3
import Adafruit_DHT
import sqlite3
import datetime
import json
import socket

# hard code GPIO pin used
GPIO_PIN = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
print('[INFO] Reading sensor data...')
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, GPIO_PIN)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
if humidity is not None and temperature is not None:

    print('[INFO] Reading config file...')
    with open('./config.json') as config_file:
        cfg = json.load(config_file)

    print('[INFO] Connecting to DB...')
    conn = sqlite3.connect(cfg['dbFileName'])

    print('[INFO] Saving to DB...')
    cur = conn.cursor()
    db_vals = (humidity, temperature, socket.gethostname(), datetime.datetime.now())
    conn.execute("INSERT INTO measurements (temp, hum, device, ts) VALUES (?, ?, ?, ?)", db_vals)
    conn.commit()
    conn.close()
    print('[INFO] DONE')
    