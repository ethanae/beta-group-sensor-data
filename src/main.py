#!/usr/bin/python
import soil
import bmp180
import hmac
import hashlib
import base64
import urllib
import time
import requests
import json
import argparse
import csv
from datetime import datetime

def get_readings():
	return { 
	    'bmp': bmp180.get_readings(),
    	    'soil': soil.get_reading()
        }

# get_readings()

parser = argparse.ArgumentParser(description='')
parser.add_argument('--key', type=str, 
                    help='SAWS API key')
parser.add_argument('--isTrial', type=bool,
                    help='Is this a strial account?')
args = parser.parse_args()

def get_weather_data():
    key = args.key
    webservice = 'weather.measurements.getByCoord'
    useTrial = args.isTrial
    useTimestamp = True

    queryString = 'location=-33.9417555,18.4244712&groups=basic,extended,astronomical,tides'
    message = queryString + '/' + webservice + '/' + key

    timestamp = str(int(time.time()))
    if (useTimestamp):
        message = message + '/' + timestamp

    if (useTrial):
        authCode = 'trial'
    else:
        digest = hmac.new(key=secret, msg=message, digestmod=hashlib.sha1).digest()
        base64 = base64.b64encode(digest).decode()
        authCode = base64.replace('+','-').replace('/','_').replace('=','')

    baseUrl = 'https://saas.afrigis.co.za/rest/2/'
    request = baseUrl + webservice + '/' + key + '/' + authCode
    if (useTimestamp):
        request = request + '/' + timestamp

    request = request + '/?' + queryString
    res = requests.get(request)
    print(res)
    return json.loads(res.content)

def write_sensor_data():
    data = {}
    weather_data = get_weather_data()['result'][0]['station_readings'][0]
    print(weather_data)
    sensorData = get_readings()
    data['Temprature'] = sensorData['bmp']['temp']
    data['Pressure'] = sensorData['bmp']['pressure']
    data['Altitude'] = sensorData['bmp']['altitude']
    data['Soil Moisture'] = sensorData['soil']
    data['Irrigation'] = sensorData['soil']
    now = datetime.now()
    fileName = "%s_%s_%s.csv" % (now.year, now.month, now.day)
    with open(fileName, 'w') as csvfile:
        fieldnames = ['Date', 'Temprature', 'Pressure', 'Altitude', 'Sea level', 'Soil Moisture', 'Humidity', 'wind_speed', 'rainfall', 'Irrigation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
	writer.writeheader() 
       	data['Date'] = now.today().strftime("%d/%m/%Y %H:%M")
        data['Sea level'] = ''
        data['Humidity'] = weather_data['humidity']
        data['wind_speed'] = weather_data['wind_speed']
        data['rainfall'] = weather_data['last_hours_rainfall']
        print(data)
        writer.writerow(data)

write_sensor_data()
