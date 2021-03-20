import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
	#url = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=8854d5ab00416d12b32c4da01e2d86d7'
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=271d1234d3f497eed5b1d80a07b3fcd1'
	# city = 'Lagos'
	form = CityForm()

	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')
	

	cities = City.objects.all()

	#empyth list for data of all cities to be collected
	weather_data = []

	for city in cities:

		#data return from the api call, convert to a json file
		r = requests.get(url.format(city)).json()

		city_weather = {
			'city': city.name,
			'temprature': r['main']['temp'],
			'description': r['weather'][0]['description'],
			'icon': r['weather'][0]['icon'],
		}

		#appened information for each city to the list
		weather_data.append(city_weather)

	# print(weather_data)

	context = {'weather_data': weather_data, 'form': form}
	return render(request, 'weather/weather.html', context)

def deleteCity(request, pk):
	city = City.objects.get(name=pk)

	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=271d1234d3f497eed5b1d80a07b3fcd1'

	r = requests.get(url.format(city)).json()

	city_weather = {
		'city': city.name,
		'temprature': r['main']['temp'],
		'description': r['weather'][0]['description'],
		'icon': r['weather'][0]['icon'],
	}

	if request.method =="POST":
		city.delete()
		return redirect('/')

	context = {'city_weather': city_weather}
	return render(request, 'weather/delete.html', context)
