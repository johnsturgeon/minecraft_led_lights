import random

from adafruit_led_animation.animation import Animation
import time

from adafruit_led_animation.color import BLACK


class ColorCycle(Animation):
    """
    Animate a sequence of one or more colors, cycling at the specified speed.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param colors: A list of colors to cycle through in ``(r, g, b)`` tuple, or ``0x000000`` hex
                   format. Defaults to a rainbow color cycle.
    """

    def __init__(self, pixel_object, speed, colors=(0, 255, 0), name=None):
        self.colors = colors
        super().__init__(pixel_object, speed, colors[0], name=name)
        self._generator = self._color_generator()
        next(self._generator)

    on_cycle_complete_supported = True

    def draw(self):
        self.pixel_object.fill(self.color)
        next(self._generator)

    def _color_generator(self):
        index = 0
        while True:
            self._color = self.colors[index]
            yield
            index = (index + 1) % len(self.colors)
            if index == 0:
                self.cycle_complete = True

    def reset(self):
        """
        Resets to the first color.
        """
        self._generator = self._color_generator()


class Rain(ColorCycle):
    """
    Blink a color on and off.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    """

    def __init__(self, pixel_object, is_stopping=False):
        self.is_stopping = is_stopping
        self.rain_sky_color = (0, 3, 9)
        self.splash_color = (0, 12, 50)
        self.num_rain_drops = len(pixel_object) // 4
        super().__init__(pixel_object, 0.2, self.rain_sky_color)
        self.fill(self.rain_sky_color)
        self.show()

    def draw(self):
        # generate random raindrops
        if self.is_stopping:
            while self.num_rain_drops > 2:
                self.num_rain_drops = self.num_rain_drops - 5
                self.do_rain_effect()
                self.show()
                time.sleep(0.1)
            return
        self.do_rain_effect()

    def do_rain_effect(self):
        self.fill(self.rain_sky_color)
        for i in range(self.num_rain_drops):
            self.pixel_object[
                random.randrange(0, len(self.pixel_object))
            ] = self.splash_color


    def reset(self):
        self.fill(self.rain_sky_color)
