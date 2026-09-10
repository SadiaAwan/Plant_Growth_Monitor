from machine import ADC, Pin, PWM

# Simulated soil moisture sensor
moisture_sensor = ADC(Pin(26))

# RGB LED
red = PWM(Pin(13))
green = PWM(Pin(12))

red.freq(1000)
green.freq(1000)

def read_moisture():
    raw_value = moisture_sensor.read_u16()
    moisture_percent = raw_value / 65535 * 100

    return moisture_percent

def set_color(r, g):
  red.duty_u16(r)
  green.duty_u16(g)

def set_moisture_color(moisture):
    if moisture < 30:
        print("STATUS: DRY")
        set_color(0, 65535)

    elif moisture < 70:
        print("STATUS: OK")
        set_color(0, 0)

    else:
        print("STATUS: GOOD")
        set_color(65535, 0)