from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    app_id = '169e8e5372a77332361671769180da9b'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
            'main': res['weather'][0]['main']
        }
        # all_cities.append(city_info)
        if len(all_cities) < 3:
            all_cities.append(city_info)
        else:
            all_cities = []
            all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form
    }

    return render(request, 'weather/index.html', context)