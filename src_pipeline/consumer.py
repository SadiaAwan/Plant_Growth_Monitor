import json
import os
import paho.mqtt.client as mqtt
from utils.connect_postgres import query_db


MQTT_BROKER ="mosquitto"
MQTT_PORT = 1883
TOPIC = "plant-monitor/sensors"

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    moisture = float(data["moisture"])
    distance = float(data["distance"])
    plant_height = float(data["plant_height"])
    growth = float(data["growth"])

    query_db(
        """
        INSERT INTO sensor_readings (
        time,
        moisture,
        distance_cm,
        plant_height_cm,
        growth_cm
        )
        VALUES (NOW(), %s, %s, %s, %s)
        """,
        (
            moisture,
            distance,
            plant_height,
            growth,
        ),
    )

    print(
        "Recevied:",
        moisture,
        distance,
        plant_height,
        growth
    )

if __name__ == "__main__":

    # Check MQTT credentials
    if not MQTT_USER or not MQTT_PASSWORD:
        raise RuntimeError("MQTT_USER or MQTT_PASSWORD is missing")

    query_db(
        """
        CREATE TABLE IF NOT EXISTS sensor_readings (
            time TIMESTAMPTZ NOT NULL,
            moisture DOUBLE PRECISION,
            distance_cm DOUBLE PRECISION,
            plant_height_cm DOUBLE PRECISION,
            growth_cm DOUBLE PRECISION
        )
        """
    )

    # Convert the PostgreSQL table into a TimescaleDB hypertable
    query_db(
        """
        SELECT create_hypertable(
            'sensor_readings',
            'time',
            if_not_exists => TRUE
        )
        """
    )

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    client.username_pw_set(
        MQTT_USER,
        MQTT_PASSWORD
    )

    client.on_message = on_message

    client.connect(
        MQTT_BROKER,
        MQTT_PORT,
        60,
    )

    client.subscribe(TOPIC)

    print(f"Subscribed to {TOPIC}")

    client.loop_forever()