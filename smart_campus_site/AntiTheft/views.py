from django.shortcuts import render
from .models import OnOff, BreakEvent
from . import iot_mqtt
import paho.mqtt.publish as publish
import json
from django.http import HttpResponse

# Create your views here.
def index(request):
    onoff = OnOff.objects.values('state').order_by('-date_ordered').first()['state']
    Breaking = BreakEvent.objects.values('Break').order_by('-date_ordered').first()['Break']

    context = {'onoff': onoff, 'Breaking':Breaking}
    mqtt_payload = {"state": onoff}
    mqtt_topic = "OnOFF"
    # Publish message to MQTT broker
    publish.single(mqtt_topic, payload=json.dumps(mqtt_payload), hostname="broker.hivemq.com")
    return render(request, 'AntiTheft/index.html', context) # Pass the context to HTML template

def publish_on_off(request):
    # Get current state from form data
    state = request.POST.get('state')
    
    mqtt_payload = {"state": state}
    mqtt_topic = "OnOFF"
    
    # Publish message to MQTT broker
    publish.single(mqtt_topic, payload=json.dumps(mqtt_payload), hostname="broker.hivemq.com")
    return HttpResponse(status=204)