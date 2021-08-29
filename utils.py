from datetime import datetime
import requests

OPENWEATHER_API_KEY = 'cfb278db7e23d4b26702d3edd4494800'

def current_weather():
    CITY_ID = 5283054 # Branford, CT as closest city
    res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&appid={OPENWEATHER_API_KEY}&units=imperial')

    current_weather = res.json()

    outside_temperature = current_weather["main"]["temp"]
    outside_humidity = current_weather["main"]["humidity"]

    return outside_temperature, outside_humidity

def timeoffset(ts):
    date = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
    now = datetime.utcnow()
    diff_in_seconds = round((now - date).total_seconds())

    if diff_in_seconds < 60:
        return f'{diff_in_seconds} s ago'
    elif diff_in_seconds < 60*60:
        return f'{round(diff_in_seconds/60)} min ago'
    elif diff_in_seconds < 24*60*60:
        return f'{round(diff_in_seconds/60/60)} hr ago'
    elif diff_in_seconds < 7*24*60*60:
        days = round(diff_in_seconds/60/60/24)
        if days > 1:
            return f'{days} days ago'
        else:
            return f'1 day ago'
    else:
        weeks = round(diff_in_seconds/60/60/24/7)
        if weeks > 1:
            return f'{weeks} weeks ago'
        else:
            return f'1 week ago'