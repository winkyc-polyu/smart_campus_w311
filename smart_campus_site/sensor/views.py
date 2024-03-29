from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from sensor.models import Sensor
from django.db.models import Max, Min, Avg
from . import sensor_mqtt


def index(request):
    context = {'nav_class' : 'nav_sensor'}
    return render(request, 'sensor/index.html', context)

    
def temp_data(request):
    LIMITED = 500
    sensors = Sensor.objects.all().order_by('-date_created')[:LIMITED][::-1]

    data = serializers.serialize('json', sensors)
    return JsonResponse(data, safe=False)

def temp_info(request):
    info = Sensor.objects.values('node_id', 'node_loc').annotate(
        last_updated=Max('date_created'),
        max_temp=Max('temp'), min_temp=Min('temp'), avg_temp=Avg('temp'),
        )
    context = {'info' : info, 'nav_class' : 'nav_summary'}
    return render(request, 'sensor/temp_info.html', context)
    
def hum_info(request):
    info = Sensor.objects.values('node_id', 'node_loc').annotate(
        last_updated=Max('date_created'),
        max_hum=Max('hum'), min_hum=Min('hum'), avg_hum=Avg('hum')
        )
    context = {'info' : info, 'nav_class' : 'nav_summary'}
    return render(request, 'sensor/hum_info.html', context)
    
def light_info(request):
    info = Sensor.objects.values('node_id', 'node_loc').annotate(
        last_updated=Max('date_created'),
        max_light=Max('light'), min_light=Min('light'), avg_light=Avg('light')
        )
    context = {'info' : info, 'nav_class' : 'nav_summary'}
    return render(request, 'sensor/light_info.html', context)
    
def snd_info(request):
    info = Sensor.objects.values('node_id', 'node_loc').annotate(
        last_updated=Max('date_created'),
        max_snd=Max('snd'), min_snd=Min('snd'), avg_snd=Avg('snd'),
        )
    context = {'info' : info, 'nav_class' : 'nav_summary'}
    return render(request, 'sensor/snd_info.html', context)