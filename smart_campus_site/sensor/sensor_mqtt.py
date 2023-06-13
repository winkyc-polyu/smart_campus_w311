import paho.mqtt.client as mqtt
from .models import Sensor
import json
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg

logger = logging.getLogger('django')

from django.core.mail import EmailMessage


def sendemail(value, type, des, loc, unit, avg):
    subject = 'Outlier Notification'
    
    # Calculate the percentage for the bar chart
    max_value = max(value, avg)
    value_percentage = (value / max_value) * 100
    avg_percentage = (avg / max_value) * 100

    message = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .red-text {{
                    color: red;
                }}
                .bar-chart {{
                    display: flex;
                    justify-content: space-between;
                    height: 300px;
                    max-height: 300px;
                }}
                .bar-container {{
                    width: 50%;
                    padding: 0 2px;
                    display: flex;
                    justify-content: center;
                    align-items: flex-end;
                }}
                .bar {{
                    width: 50%;
                    text-align: center;
                }}
                .value-bar {{
                    background-color: red;
                    height: {value_percentage}%;
                }}
                .average-bar {{
                    background-color: #4CAF50;
                    height: {avg_percentage}%;
                }}
            </style>
        </head>
        <body>
            <h1><span class="red-text">! Detect unexpected Change</span></h1>
            <p>{type} anomaly detected--{des} {value} {unit} in {loc}<br>
            The average {type} is {avg:.2f} {unit}</p>
            <p>Comparison:</p>
            <div class="bar-chart">
                <div class="bar-container">
                    <div class="bar value-bar" style="height: {value_percentage}%;">Value: {value} {unit}</div>
                </div>
                <div class="bar-container">
                    <div class="bar average-bar" style="height: {avg_percentage}%;">Average: {avg:.2f} {unit}</div>
                </div>
            </div>
        </body>
        </html>
    '''

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [admin[1] for admin in settings.ADMINS]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'  # Set the email content type as HTML
    email.send()


def mqtt_on_message(client, userdata, msg):
    d_msg = str(msg.payload.decode("utf-8"))
    iotData = json.loads(d_msg)
    #if iotData["node_id"] == ID:
    print("Received message on topic %s : %s" % (msg.topic, iotData))
    p = Sensor(node_id=iotData["node_id"], node_loc=iotData["loc"], 
        temp=iotData["temp"], hum=iotData["hum"], light=iotData["light"], snd=iotData["snd"])
    p.save()
    send(p)

def send(p):
    inf=Sensor.objects.values('node_id','node_loc').annotate(avg_temp=Avg('temp'),avg_hum=Avg('hum'),avg_light=Avg('light'),avg_snd=Avg('snd'))
    p.temp=int(p.temp)
    p.hum=int(p.hum)
    p.light=int(p.light)
    p.snd=int(p.snd)
    for i in inf:
        if p.node_id==i['node_id']:
            if p.temp>i['avg_temp']+10:
                sendemail(p.temp,'Temperature','High Temperature',p.node_loc,"\u2103",i['avg_temp'])
            elif p.temp<i['avg_temp']-10:
                sendemail(p.temp,'Temperature','Low Temperature',p.node_loc,"\u2103",i['avg_temp'])
            if p.hum>i['avg_hum']+15:
                sendemail(p.hum,'Humidity','High Humidity',p.node_loc,"%",i['avg_hum'])
            elif p.hum<i['avg_hum']-15:
                sendemail(p.hum,'Humidity','Low Humidity',p.node_loc,"%",i['avg_hum'])
            if p.light>i['avg_light']+10:
                sendemail(p.light,'Light','Intense Light',p.node_loc,"%",i['avg_light'])
            elif p.light<i['avg_light']-30:
                sendemail(p.temp,'Light','Dark',p.node_loc,"%",i['avg_light'])
            if p.snd>i['avg_snd']+20:
                sendemail(p.temp,'Sound','Loud sound',p.node_loc,"dB",i['avg_snd'])
            elif p.snd<i['avg_snd']-10:
                sendemail(p.temp,'Sound','Silent',p.node_loc,"dB",i['avg_snd'])
        else:
            pass


ID="A01" # Sensor ID
mqtt_broker = "broker.hivemq.com" # Broker
mqtt_port = 1883 # Default
mqtt_qos = 1 # Quality of Service = 1
mqtt_topic = "iot/sensor-A"


mqtt_client = mqtt.Client("django-sensor-A011") # Create a Client Instance
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect(mqtt_broker, mqtt_port) # Establish a connection to a broker
print("Connect to MQTT broker")
mqtt_client.subscribe(mqtt_topic, mqtt_qos)

mqtt_client.loop_start()