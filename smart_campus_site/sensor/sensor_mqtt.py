import paho.mqtt.client as mqtt
from .models import Sensor
import json

def mqtt_on_message(client, userdata, msg):
    d_msg = str(msg.payload.decode("utf-8"))
    iotData = json.loads(d_msg)
    if iotData["id"] == ID:
        print("Received message on topic %s : %s" % (msg.topic, iotData))
        p = Sensor(node_id=iotData["id"], node_loc=iotData["loc"], 
            temp=iotData["temp"], hum=iotData["hum"], light=iotData["light"], snd=iotData["snd"])
        p.save()

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