import time
from plant_display import PlantDisplay
from moisture import read_moisture, set_moisture_color
from buzzer import play_alert
from distance import read_distance, calculate_plant_height, calculate_growth

# from wifi import connect_wifi
# from sensor import read_light
# from mqtt import connect_mqtt, publish_light

time.sleep(0.1) # Wait for USB to become ready

print("Plant monitor started")

display = PlantDisplay()

alert_played = False

while True:
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

    time.sleep(1)