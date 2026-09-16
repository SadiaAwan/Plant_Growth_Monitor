import json
import network
import rp2
import time
from machine import Pin


rp2.country("SE")

with open("wifi_credentials.json") as file:
    credentials = json.load(file)

WIFI_SSID = credentials.get("WIFI_SSID")
WIFI_PASSWORD = credentials.get("WIFI_PASSWORD")

wifi_led = Pin(15, Pin.OUT)
wifi_led.value(0)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect_wifi(waiting_time=10):

    if wlan.isconnected():
        wifi_led.value(1)

        print("Already connected to WiFi")
        print(f"IP:{wlan.ifconfig()[0]}")

        return wlan

    print("Connecting to WiFi...")

    wlan.connect(
        WIFI_SSID, 
        WIFI_PASSWORD
        )


    while waiting_time > 0:
        if wlan.isconnected():
            wifi_led.value(1)
            print("Connected to WiFi!")
            print(f"IP:{wlan.ifconfig()}")
            return wlan

        print("Trying to connect wifi, pls wait")
        time.sleep(2)
        waiting_time -= 1

    print("Could not connect to WiFi")

    return None

def is_wifi_connected():
    if wlan.isconnected():
        wifi_led.value(1)
        return True

    wifi_led.value(0)
    return False

def ensure_wifi():
    if is_wifi_connected():
        return True

    print("WiFi connection lost")
    print("Trying to reconnect...")

    connection = connect_wifi()

    if connection is not None:
        return True

    return False