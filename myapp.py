from flask import Flask, render_template, request, jsonify
import json
import requests
from pprint import pprint
from functools import wraps
from flask import  Response


def check_auth(username, password):
    return username == 'identification1' and password == 'weather'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)

@app.route("/")
@requires_auth
def index():
    return render_template("index.html")

weather_url_template ='https://api.weatherbit.io/v2.0/history/hourly?city={city}&start_date={start}&end_date={end}&tz=local&key={key}'

@app.route('/weatherstat', methods=['GET', 'POST'])
def weatherinfo():
    my_api_key = request.args.get('key','00c0f94fd8884f6499d4e7644657015a')
    my_city = request.form.get('city')
    start_date = request.form.get ('start')
    end_date = request.form.get ('end')
    hour = request.form.get('hour')

    weather_url = weather_url_template.format(key = my_api_key, city = my_city, start = start_date, end = end_date)

    resp= requests.get(weather_url)
    if resp.ok:
            showweather = resp.json()
            if hour.lower() != 'all':
                data = showweather['data']
                for item in data:
                    if item["timestamp_local"] == start_date + "T{0:0=2d}:00:00".format(int(hour)):
                        data = item
                        break
                showweather['data'] = data
    else:
            print(resp.reason)

    return jsonify(showweather)

if __name__ == "__main__":
    app.run( debug = True )

