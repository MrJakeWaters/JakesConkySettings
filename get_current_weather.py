#!/usr/bin/python3

import json
import math
import datetime
import openmeteo_requests
from datetime import timedelta
from plyer import notification
from openmeteo_sdk.Variable import Variable

def get_wind_direction(degrees):
    # function takes input where 360 > degrees >= 0
    # and returns N/NE/E/SE/SW/NW
    quadrant = math.floor(degrees/90)
    oriented_degrees = round(((degrees/90) - quadrant)*90, 2)
    compass_map = {
        "0": "°N",
        "1": "°E",
        "2": "°S",
        "3": "°W"
    }
    output = {
        'degrees': oriented_degrees
    }
    if oriented_degrees == 0:
        output['direction'] = compass_map[str(int(quadrant))]
    else:
        if quadrant == 0:
            output['direction'] = 'NE'
        elif quadrant == 1:
            output['direction'] = 'SE'
        elif quadrant == 2:
            output['direction'] = 'SW'
        elif quadrant == 3:
            output['direction'] = 'NE'
        else:
            raise Exception('Something went wrong')
    return output

om = openmeteo_requests.Client()
params = {
	"latitude": 39.6166,
	"longitude": -105.2372,
	"current": ["temperature_2m", "relative_humidity_2m", "showers", "rain", "precipitation", "snowfall", "wind_speed_10m", "wind_direction_10m"],
	"wind_speed_unit": "mph",
    "temperature_unit": "fahrenheit",
	"precipitation_unit": "inch"
}

url = "https://api.open-meteo.com/v1/forecast"
responses = om.weather_api(url, params=params)
response = responses[0]

current = response.Current()
output = {
        "refresh_ts": datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
}
for i,x in enumerate(params['current']):
    output[x] = round(current.Variables(i).Value(), 1)
wind = get_wind_direction(output['wind_direction_10m'])
output['wind_direction'] = wind['direction']
output['wind_direction_degrees'] = wind['degrees']
print(json.dumps(output))
