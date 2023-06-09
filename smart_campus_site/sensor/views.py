from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from sensor.models import Sensor
from . import sensor_mqtt


def index(request):
    return render(request, 'sensor/index.html')

    
def temp_data(request):
    sensors = Sensor.objects.all()
    data = serializers.serialize('json', sensors)
    return JsonResponse(data, safe=False)