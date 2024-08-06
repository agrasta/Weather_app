from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
api_key = '279d3391dddf51cbe4237785fc3c8042'
weather_url = 'http://api.openweathermap.org/data/2.5/weather'
autocomplete_url = 'http://api.openweathermap.org/data/2.5/find'

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    params = {
        'q': query,
        'type': 'like',
        'sort': 'population',
        'appid': api_key
    }

    response = requests.get(autocomplete_url, params=params)
    response.raise_for_status()
    data = response.json()
    cities = [{'label': item['name'], 'value': item['name']} for item in data['list']]

    return jsonify(cities)

@app.route('/weather', methods=['GET'])
def weather_func():
    city = request.args.get('city')
    params = {
        'q': city,
        'APPID': api_key,
        'lang': 'ru',
        'units': 'metric'
    }

    response = requests.get(weather_url, params=params)
    response.raise_for_status()
    data = response.json()
    try:
        if data.get('weather'):
            return f'Погода в городе {city}: {data["weather"][0]["description"]}, температура: {data["main"]["temp"]}°C'
        else:
            return 'Не удалось получить погоду для указанного города.'
    except:
        return 'Произошла ошибка'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

