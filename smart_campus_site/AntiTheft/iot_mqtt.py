import paho.mqtt.client as mqtt
from .models import OnOff,BreakEvent
import json


mqtt_broker = "broker.hivemq.com" # Broker
mqtt_port = 1883 # Default
mqtt_qos = 1 # Quality of Service = 1
topic_onoff = "OnOFF"
topic_break = "BREAK"

def mqtt_on_message(client, userdata, msg):
    if msg.topic==topic_onoff:
        d_msg = str(msg.payload.decode("utf-8"))
        iotData = json.loads(d_msg)
        p=OnOff(state=iotData["state"])
        p.save()

    elif msg.topic==topic_break:
        d_msg = str(msg.payload.decode("utf-8"))
        iotData = json.loads(d_msg)
        p=BreakEvent(Break=iotData["detect"])
        p.save()


mqtt_client = mqtt.Client() # Create a Client Instance
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect(mqtt_broker, mqtt_port) # Establish a connection to a brokerprint("Connect to MQTT broker")
print("Connect to MQTT broker")

mqtt_client.subscribe(topic_onoff, mqtt_qos)
mqtt_client.subscribe(topic_break, mqtt_qos)
mqtt_client.loop_start()