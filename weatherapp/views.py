from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):

    city = request.POST.get('city', 'indore')
    day = datetime.date.today()

    OPENWEATHER_API_KEY = '089811b37cb013960c17cf13d369f872'

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }

    image_url = None  # Google API removed (safe & clean)

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise KeyError

        data = response.json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except Exception:
        messages.error(request, 'City information is not available from Weather API')

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': True,
            'image_url': None
        })
