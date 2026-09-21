from machine import ADC, Pin, PWM, I2C
import time

# Soil moisture sensor
i2c = I2C(
    0,
    sda=Pin(20),
    scl=Pin(21),
    freq=100000
)

SENSOR_ADDR = 0x36
DRY_VALUE = 650
WET_VALUE = 720

# RGB LED
red = PWM(Pin(13))
green = PWM(Pin(12))

red.freq(1000)
green.freq(1000)

def read_moisture_raw_once():
    i2c.writeto(SENSOR_ADDR, bytes([0x0F, 0x10]))
    time.sleep_ms(5)

    data = i2c.readfrom(SENSOR_ADDR, 2)

    raw_value = (data[0] << 8) | data[1]
    return raw_value


def read_moisture_raw():
    readings = []

    for _ in range(10):
        readings.append(read_moisture_raw_once())
        time.sleep_ms(100)

    readings.sort()

    # Median av 10 värden
    median = (readings[4] + readings[5]) / 2

    return median

def read_moisture():
    raw_value = read_moisture_raw()

    moisture_percent = (
        (raw_value - DRY_VALUE)
        / (WET_VALUE - DRY_VALUE)
        * 100
    )

    moisture_percent = max(0, min(100, moisture_percent))

    return moisture_percent

def set_color(r, g):
  red.duty_u16(r)
  green.duty_u16(g)

def set_moisture_color(moisture):
    if moisture < 30:
        print("STATUS: DRY")
        set_color(0, 65535)

    elif moisture < 65:
        print("STATUS: OK")
        set_color(0, 0)

    else:
        print("STATUS: GOOD")
        set_color(65535, 0)