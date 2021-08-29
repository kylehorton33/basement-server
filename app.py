from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

import db
import utils
from datetime import datetime

app = Flask(__name__)

def record_weather():
    outside_temp, outside_hum = utils.current_weather()
    db.new_weather_reading(outside_temp, outside_hum)
    log_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    print(f"SERVER LOG - - [{log_time}] Weather Recorded")

sched = BackgroundScheduler(daemon=True)
sched.add_job(record_weather,'interval',minutes=1)
sched.start()

@app.route('/')
def home():
    time, temp, hum = db.last_sensor_reading()
    timeoffset = utils.timeoffset(time)
    outside_temp, outside_hum = utils.current_weather()
    templateData = {
		'time': time,
		'temp': temp,
		'hum': hum,
        'timeoffset': timeoffset,
        'outside_temp': outside_temp,
        'outside_hum': outside_hum
	}
    return render_template('index.html', **templateData)

@app.route('/api/v1/new', methods=['POST'])
def new_record():
    temperature = request.get_json()["temperature"]
    humidity = request.get_json()["humidity"]
    db.new_sensor_reading(temperature, humidity)
    return jsonify("Success!")

@app.route('/api/v1/all', methods=['GET'])
def all_records():
    records = db.all_sensor_readings()
    return jsonify(records)

@app.route('/api/v1/latest', methods=['GET'])
def latest_record():
    record = db.last_sensor_reading()
    return jsonify(record)
    
        
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response
        

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=3333, debug=False)