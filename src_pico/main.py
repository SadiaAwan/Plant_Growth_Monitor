import time
from plant_display import PlantDisplay
from moisture import read_moisture, set_moisture_color
from buzzer import play_alert
from distance import read_distance, calculate_plant_height, calculate_growth
from wifi import connect_wifi, ensure_wifi
from mqtt import connect_mqtt, publish_sensor_data

time.sleep(0.1)

print("Plant monitor started")

display = PlantDisplay()

alert_played = False

wlan = connect_wifi()

mqtt_client = None

if wlan is not None:
    try:
        mqtt_client = connect_mqtt()
    except OSError as error:
        print("Could not connect to MQTT")
        print(error)

last_wifi_check = time.ticks_ms()

WIFI_CHECK_INTERVAL = 10000

while True:
    now = time.ticks_ms()

    if time.ticks_diff(now, last_wifi_check) >= WIFI_CHECK_INTERVAL:
        wifi_connected = ensure_wifi()

        last_wifi_check = now

        if wifi_connected and mqtt_client is None:
            try:
                mqtt_client = connect_mqtt()
            except OSError as error:
                print("Could not reconnect to MQTT")
                print(error)

        if not wifi_connected:
            mqtt_client = None

    moisture = read_moisture()
    distance = read_distance()
    plant_height = calculate_plant_height(distance)
    growth = calculate_growth(plant_height)

    display.update(
        moisture=moisture,
        height=plant_height,
        growth=growth
    )

    print("Moisture:", round(moisture, 1), "%")
    print("Distance:", round(distance, 1), "cm")
    print("Plant height:", round(plant_height, 1), "cm")
    print("Growth:", round(growth, 1), "cm")

    set_moisture_color(moisture)

    if moisture < 30:
        if not alert_played:
            play_alert()
            alert_played = True

    else:
        alert_played = False

    if mqtt_client is not None:
        try:
            publish_sensor_data(
                mqtt_client,
                moisture,
                distance,
                plant_height,
                growth
            )
        except OSError as error:
            print("MQTT connection lost")
            print(error)

            mqtt_client = None

    time.sleep(1)