import requests
import configparser
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    city_name = request.form['cityname']

    api_key = get_api_key()
    data = get_weather_results(city_name, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"] - 273.15)
    feels_like = "{0:.2f}".format(data["main"]["feels_like"] - 273.15)
    weather = data["weather"][0]["main"]
    location = data["name"]
    icon = data["weather"][0]["icon"]
    description = data["weather"][0]["description"]
    hdmt = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    min_temp = "{0:.2f}".format(data["main"]["temp_min"] - 273.15)
    max_temp = "{0:.2f}".format(data["main"]["temp_max"] - 273.15)
    pressure = data["main"]["pressure"]
    visibility = data["visibility"]
    clouds = data["clouds"]["all"]
    country =data["sys"]["country"]
    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]
    name = data["name"]
    date_time= datetime.now().strftime("%d %b %Y | %I:%M:%S %p")


    return render_template('results.html',date_time=date_time,min_temp=min_temp, max_temp=max_temp,
                           pressure=pressure,visibility=visibility,clouds=clouds,country=country,sunrise=sunrise,
                           sunset=sunset,name=name,
                           location=location, temp=temp,description= description,wind_speed= wind_speed,
                           feels_like=feels_like, weather=weather, icon=icon, hdmt= hdmt)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(city_name, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?q={}&appid={}".format(city_name, api_key)
    r = requests.get(api_url)
    return r.json()

if __name__ == '__main__':
    app.run()