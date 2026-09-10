import time
from machine import Pin

trigger = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN)

SENSOR_HEIGHT_CM = 40.0
INITIAL_PLANT_HEIGHT_CM = 8.0

def read_distance():
    trigger.low()
    time.sleep_us(2)

    trigger.high()
    time.sleep_us(10)

    trigger.low()

    while echo.value() == 0:
        pulse_start = time.ticks_us()
    
    while echo.value() == 1:
        pulse_end = time.ticks_us()
    
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)

    distance_cm = pulse_duration * 0.0343 / 2

    return distance_cm

def calculate_plant_height(distance_cm):
    plant_height = SENSOR_HEIGHT_CM - distance_cm

    return max(0, plant_height)

def calculate_growth(plant_height):
    growth = plant_height - INITIAL_PLANT_HEIGHT_CM

    return max(0, growth)

