import time
from machine import Pin, PWM

buzzer = PWM(Pin(14))
buzzer.duty_u16(0)


def play_alert():
    melody = [
        (659, 0.15),
        (587, 0.15),
        (370, 0.30),
        (415, 0.30),

        (554, 0.15),
        (494, 0.15),
        (294, 0.30),
        (330, 0.30),

        (494, 0.15),
        (440, 0.15),
        (277, 0.30),
        (330, 0.30),

        (440, 0.45),
    ]

    for frequency, duration in melody:
        buzzer.freq(frequency)
        buzzer.duty_u16(18000)

        time.sleep(duration)

        buzzer.duty_u16(0)
        time.sleep(0.05)