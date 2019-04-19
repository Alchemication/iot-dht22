#!/usr/bin/python3
import Adafruit_DHT
import sqlite3
import datetime
import json
import socket

def read_config():

    # get params from config file
    print('[INFO] Reading config file...')
    with open('/home/pi/Laboratory/iot-dht22/config.json') as config_file:
        return json.load(config_file)

def probe_sensor(cfg):

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    print('[INFO] Reading sensor data...')
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, cfg['gpioPin'])

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    if humidity is not None and temperature is not None:
        return (humidity, temperature)
    return None

def save_to_db(cfg, sensor_vals):

    if sensor_vals is None:
        print('[WARNING] Sensor values not received, stopping early...')
        return

    # unpack sensor values
    humidity, temperature = sensor_vals

    print('[INFO] Connecting to DB...')
    conn = sqlite3.connect(cfg['dbFileName'])

    print('[INFO] Saving to DB...')
    cur = conn.cursor()
    db_vals = (humidity, temperature, socket.gethostname(), datetime.datetime.now())
    conn.execute("INSERT INTO measurements (temp, hum, device, ts) VALUES (?, ?, ?, ?)", db_vals)
    conn.commit()
    conn.close()
    print('[INFO] DONE')

if __name__ == '__main__':
    cfg = read_config()
    sensor_vals = probe_sensor(cfg)
    save_to_db(cfg, sensor_vals)