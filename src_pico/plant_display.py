from machine import Pin, I2C
from lib.ssd1306 import SSD1306_I2C
import time


class PlantDisplay:
    def __init__(self, switch_interval=4000):
        self.i2c = I2C(
            1,
            scl=Pin(19),
            sda=Pin(18),
            freq=400000
        )

        self.oled = SSD1306_I2C(128, 64, self.i2c)

        self.current_page = 0
        self.last_switch = time.ticks_ms()
        self.switch_interval = switch_interval


    def update(self, moisture, height, growth):
        """Uppdaterar displayen och byter sida automatiskt."""

        now = time.ticks_ms()

        if time.ticks_diff(now, self.last_switch) >= self.switch_interval:
            self.current_page = 1 - self.current_page
            self.last_switch = now

        if self.current_page == 0:
            self.show_moisture(moisture)
        else:
            self.show_growth(height, growth)


    def show_moisture(self, moisture):
        self.oled.fill(0)

        self.oled.text("SOIL MOISTURE", 12, 0)

        # Enkel droppsymbol
        self.draw_drop(36, 20)

        self.oled.text("{}%".format(int(moisture)), 60, 18)

        if moisture < 30:
            status = "DRY"
        elif moisture < 60:
            status = "OK"
        else:
            status = "GOOD"

        self.oled.text(status, 60, 30)

        # Progress bar
        self.draw_progress_bar(moisture)

        self.draw_page_indicator(0)

        self.oled.show()


    def show_growth(self, height, growth):
        self.oled.fill(0)

        self.oled.text("PLANT GROWTH", 12, 0)

        # Enkel planta
        self.draw_plant(14, 22)

        self.oled.text("{:.1f} cm".format(height), 42, 18)
        self.oled.text("+{:.1f} cm".format(growth), 42, 31)

        if growth > 0.5:
            status = "GROWING"
        elif growth > 0:
            status = "STABLE"
        else:
            status = "NO GROWTH"

        self.oled.text(status, 42, 45)

        self.draw_page_indicator(1)

        self.oled.show()


    def draw_progress_bar(self, value):
        value = max(0, min(100, value))

        x = 5
        y = 48
        width = 118
        height = 9

        self.oled.rect(x, y, width, height, 1)

        fill_width = int((width - 4) * value / 100)

        if fill_width > 0:
            self.oled.fill_rect(
                x + 2,
                y + 2,
                fill_width,
                height - 4,
                1
            )


    def draw_drop(self, x, y):
        """Enkel pixel-art vattendroppe."""

        self.oled.line(x + 6, y, x, y + 10, 1)
        self.oled.line(x, y + 10, x, y + 15, 1)
        self.oled.line(x, y + 15, x + 6, y + 20, 1)

        self.oled.line(x + 6, y, x + 12, y + 10, 1)
        self.oled.line(x + 12, y + 10, x + 12, y + 15, 1)
        self.oled.line(x + 12, y + 15, x + 6, y + 20, 1)


    def draw_plant(self, x, y):
        """Enkel planta med stam och blad."""

        # Stam
        self.oled.line(x + 8, y + 8, x + 8, y + 27, 1)

        # Vänster blad
        self.oled.line(x + 8, y + 13, x, y + 8, 1)
        self.oled.line(x, y + 8, x + 3, y + 16, 1)
        self.oled.line(x + 3, y + 16, x + 8, y + 13, 1)

        # Höger blad
        self.oled.line(x + 8, y + 10, x + 16, y + 5, 1)
        self.oled.line(x + 16, y + 5, x + 14, y + 14, 1)
        self.oled.line(x + 14, y + 14, x + 8, y + 10, 1)

        # Jord
        self.oled.line(x, y + 28, x + 17, y + 28, 1)


    def draw_page_indicator(self, page):
        """Två små indikatorer längst ner till höger."""

        if page == 0:
            self.oled.fill_rect(112, 60, 4, 3, 1)
            self.oled.rect(120, 60, 4, 3, 1)
        else:
            self.oled.rect(112, 60, 4, 3, 1)
            self.oled.fill_rect(120, 60, 4, 3, 1)