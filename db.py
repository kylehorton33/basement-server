import sqlite3

DATABASE = 'data/sensorsData.db'

def connect():
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    return conn, curs

def disconnect(conn):
    conn.commit()
    conn.close()

def new_sensor_reading(temp, hum):
    conn, curs = connect()
    curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
    disconnect(conn)

def all_sensor_readings():
    conn, curs = connect()
    curs.execute("SELECT * FROM DHT_data")
    return curs.fetchall()

def last_sensor_reading():
    conn, curs = connect()
    curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1")
    return curs.fetchone()

def new_weather_reading(outside_temp, outside_hum):
    conn, curs = connect()
    curs.execute("INSERT INTO WEATHER_data values(datetime('now'), (?), (?))", (outside_temp, outside_hum))
    disconnect(conn)