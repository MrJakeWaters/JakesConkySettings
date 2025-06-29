import os
import json
import requests
import datetime

# curl -X GET https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/39.619280,-105.245377/$(date +'%Y-%m-%dT%H:%M:%S')?key=$VISUAL_CROSSING_API_KEY | jq '.currentConditions' > /home/jacwater/.cache/weather/hourly.json

file_path = "/home/jacwater/.cache/weather/hourly.json"
ts = {
    "refresh_ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
}

api_key = os.getenv('VISUAL_CROSSING_API_KEY')
headers = {
    'content-type': 'application/json',
}

url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/39.619280,-105.245377/%s?key=%s" % (datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), api_key)
weather = requests.get(url, headers=headers).json()['currentConditions']
attributes = [
    'temp',
    'feelslike',
    'humidity',
    'precip',
    'precipprob',
    'snow',
    'snowdepth',
    'preciptype',
    'conditions'
]
weather_details = {key: weather[key] for key in attributes if key in weather}
weather_details.update(ts)

# create json file
with open(file_path, 'w') as f:
    # Write the data to the file
    json.dump(weather_details, f, indent=4)
