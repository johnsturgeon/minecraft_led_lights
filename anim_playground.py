from datetime import time
from threading import Thread
from time import sleep

from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.color import PINK

from anim_overrides import MySparkle
import light_strip

import board
import neopixel

from rain import Rain

pixel_pin = board.D18
pixel_num = 300
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)


def sparkle():
    my_sparkle = MySparkle(pixels, speed=0.05, color=(0, 50, 130), num_sparkles=20)
    while True:
        my_sparkle.animate()

def rain():
    my_rain = Rain(pixels)
    while True:
        my_rain.animate()


def sparkle_pulse():
    my_sparkle_pulse = SparklePulse(
        pixel_object=pixels,
        speed=0.001,
        color=(0, 50, 130),
        period=20,
        max_intensity=1,
        min_intensity=0
    )
    while True:
        my_sparkle_pulse.animate()

if __name__ == '__main__':
    thread = Thread(target=light_strip.raining())
    thread.start()
    # light_strip.set_brightness(0)
    # sleep(1)
    # light_strip.set_brightness(light_strip.default_brightness)
    light_strip.set_brightness(0)
    light_strip.set_brightness(0.5)
