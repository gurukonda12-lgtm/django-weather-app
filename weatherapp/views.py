from django.shortcuts import render
from django.contrib import messages
from decouple import config
import requests
import datetime


def home(request):

    if request.method == "POST":
        city = request.POST.get('city').strip()
    else:
        ip_data = requests.get("http://ip-api.com/json").json()
        city = ip_data.get("city", "Indore")

    day = datetime.date.today()

    API_KEY = "ca1a28a2e21119ea35c1a0d399bd8c0d"

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        print(data)

        if data.get("cod") != "200":
            messages.error(request, "City not found")

            return render(request, "weatherapp/index.html", {
                "exception_occurred": True
            })

        current = data["list"][0]

        description = current["weather"][0]["description"]
        icon = current["weather"][0]["icon"]
        temp = current["main"]["temp"]

        # Dynamic background
        if "cloud" in description:
            bg = "https://images.pexels.com/photos/531756/pexels-photo-531756.jpeg"
        elif "rain" in description:
            bg = "https://images.pexels.com/photos/110874/pexels-photo-110874.jpeg"
        elif "clear" in description:
            bg = "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg"
        else:
            bg = "https://images.pexels.com/photos/2559941/pexels-photo-2559941.jpeg"

        forecast_data = []

        for item in data["list"][1:6]:
            forecast_data.append({
                "time": item["dt_txt"][11:16],
                "temp": item["main"]["temp"],
                "icon": item["weather"][0]["icon"],
                "desc": item["weather"][0]["description"]
            })

        context = {
            "description": description,
            "icon": icon,
            "temp": temp,
            "day": day,
            "city": city,
            "bg": bg,
            "forecast_data": forecast_data,
            "exception_occurred": False
        }

        return render(request, "weatherapp/index.html", context)

    except Exception as e:
        print("ERROR:", e)

        return render(request, "weatherapp/index.html", {
            "description": "clear sky",
            "icon": "01d",
            "temp": 25,
            "day": day,
            "city": "Indore",
            "exception_occurred": True
        })