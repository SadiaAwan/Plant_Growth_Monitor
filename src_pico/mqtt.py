from lib.umqtt.simple import MQTTClient
import json


MQTT_BROKER = "192.168.0.100"
MQTT_PORT = 1883

CLIENT_ID = "plant-monitor-pico"
TOPIC = b"plant-monitor/sensors"


def connect_mqtt():
    client = MQTTClient(
        client_id=CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT
    )

    client.connect()

    print("Connected to MQTT broker")

    return client


def publish_sensor_data(client, moisture, distance, plant_height, growth):
    data = {
        "moisture": round(moisture, 1),
        "distance": round(distance, 1),
        "plant_height": round(plant_height, 1),
        "growth": round(growth, 1)
    }

    payload = json.dumps(data)

    client.publish(TOPIC, payload)

    print("MQTT:", payload)