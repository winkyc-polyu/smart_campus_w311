from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from sensor.models import Sensor
from django.db.models.functions import Upper
from django.db.models import Count, Max, Min, Avg
from . import sensor_mqtt


def index(request):
    return render(request, 'sensor/index.html')

    
def temp_data(request):
    sensors = Sensor.objects.all()
    data = serializers.serialize('json', sensors)
    return JsonResponse(data, safe=False)

def info(request):
    info = Sensor.objects.values('node_id', 'node_loc').annotate(
        node_loc_upper=Upper('node_loc'), last_updated=Max('date_created')
        , max_temp=Max('temp'), min_temp=Min('temp'), avg_temp=Avg('temp')
        , max_hum=Max('hum'), min_hum=Min('hum'), avg_hum=Avg('hum')
        , max_light=Max('light'), min_light=Min('light'), avg_light=Avg('light')
        , max_snd=Max('snd'), min_snd=Min('snd'), avg_snd=Avg('snd'),
        )
    context = {'info' : info} # Store the data in "context" dictionaries
    return render(request, 'sensor/info.html', context) # Pass the context to HTML template