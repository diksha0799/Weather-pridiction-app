import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=541a33382e54423fc27a4bc7c71ca1a6'
    # q is the city variable that's gonna be queried in
     
    err_msg =''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'
        if err_msg:
            message = err_msg 
            message_class = 'is_danger'
        else:
            message = 'City added successfully!'
            message_class = 'is_success'

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        #this is the use of the api to get the details

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    # print(weather_data)

    
    context = {'weather_data' : weather_data,
     'form' : form, 
     'message' : message, 
     'message_class': message_class
    }
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')
