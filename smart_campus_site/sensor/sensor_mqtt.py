import paho.mqtt.client as mqtt
from .models import Sensor
import json
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg
logger = logging.getLogger('django')

from django.core.mail import EmailMessage

import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from django.core.mail import EmailMessage
# ...

import io
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
from .models import Sensor
import json
import logging
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Avg


logger = logging.getLogger('django')

import numpy as np

from email.mime.image import MIMEImage


logger = logging.getLogger('django')



logger = logging.getLogger('django')

def sendemail(value, type, des, loc, unit, avg):
    subject = 'Outlier Notification'
    message = f'{type} anomaly detected -- {des} {value} {unit} in {loc}\nThe average {type} is {avg:.2f} {unit}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [admin[1] for admin in settings.ADMINS]
    try:
        fig, ax = plt.subplots()
        ax.bar(["value", "avg"], [value, avg], color=["orange", "blue"])
        ax.set_title(f"{type} Anomaly")
        ax.set_ylabel(unit)
        chart_buffer = io.BytesIO()
        plt.savefig(chart_buffer, format='png')
        chart_buffer.seek(0)
        chart_filename = f"{type}_anomaly_chart.png"
        email_msg = EmailMessage(subject, message, from_email, recipient_list)
        email_msg.attach(chart_filename, chart_buffer.getvalue(), 'image/png')
        email_msg.send()
        logger.info(f"Email sent successfully to {recipient_list}")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")

def mqtt_on_message(client, userdata, msg):
    d_msg = str(msg.payload.decode("utf-8"))
    iotData = json.loads(d_msg)
    #if iotData["node_id"] == ID:
    print("Received message on topic %s : %s" % (msg.topic, iotData))
    p = Sensor(node_id=iotData["node_id"], node_loc=iotData["loc"],temp=iotData["temp"], hum=iotData["hum"], light=iotData["light"], snd=iotData["snd"])
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
            if p.hum>i['avg_hum']+20:
                sendemail(p.hum,'Humidity','High Humidity',p.node_loc,"%",i['avg_hum'])
            elif p.hum<i['avg_hum']-20:
                sendemail(p.hum,'Humidity','Low Humidity',p.node_loc,"%",i['avg_hum'])
            if p.light>i['avg_light']+10:
                sendemail(p.light,'Light','Intense Light',p.node_loc,"%",i['avg_light'])
            elif p.light<i['avg_light']-30:
                sendemail(p.temp,'Light','Dark',p.node_loc,"%",i['avg_light'])
            if p.snd>i['avg_snd']+20:
                sendemail(p.temp,'Sound','Loud sound',p.node_loc,"dB",i['avg_snd'])
            elif p.snd<i['avg_snd']-10:
                pass


ID="A01" # Sensor ID
mqtt_broker = "broker.hivemq.com" # Broker
mqtt_port = 1883 # Default
mqtt_qos = 1 # Quality of Service = 1
mqtt_topic = "iot/sensor-A"


mqtt_client = mqtt.Client("django-sensor-A01") # Create a Client Instance
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect(mqtt_broker, mqtt_port) # Establish a connection to a broker
print("Connect to MQTT broker")
mqtt_client.subscribe(mqtt_topic, mqtt_qos)

mqtt_client.loop_start()