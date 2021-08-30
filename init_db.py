import sqlite3

conn = sqlite3.connect('data/database.db')

conn.execute('CREATE TABLE IF NOT EXISTS DHT_data (timestamp DATETIME, temp NUMERIC, hum NUMERIC)')
conn.execute('CREATE TABLE IF NOT EXISTS WEATHER_data (timestamp DATETIME, temp NUMERIC, hum NUMERIC)')

conn.close()