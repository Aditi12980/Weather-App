from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "5943e39507ddd16b36a59d7fee8401d1"


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url).json()

        if response.get("cod") != 200:
            return None

       
        forecast_data = []
        for item in forecast_response["list"]:
            if "12:00:00" in item["dt_txt"]:
                forecast_data.append({
                    "temp": item["main"]["temp"],
                    "desc": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"],
                    "day": item["dt_txt"].split(" ")[0]
                })

        return {
            "city": city,
            "temperature": response["main"]["temp"],
            "humidity": response["main"]["humidity"],
            "description": response["weather"][0]["description"],
            "icon": response["weather"][0]["icon"],
            "forecast": forecast_data
        }

    except Exception as e:
        print("Error:", e)
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    cities_weather = []

    cities = ["Pune", "Mumbai"]

    if request.method == 'POST':
        cities_input = request.form.get('city')
        cities = [c.strip() for c in cities_input.split(',')]

    for city in cities:
        data = get_weather(city)
        if data:
            cities_weather.append(data)

    return render_template('index.html', cities_weather=cities_weather)


@app.route('/location')
def location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        city = response.get("name")
        data = get_weather(city)

        return render_template('index.html', cities_weather=[data])

    except:
        return render_template('index.html', cities_weather=[])


if __name__ == '__main__':
    app.run(debug=True)