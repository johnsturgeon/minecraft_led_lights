import time
from typing import List

import board
import neopixel

from light_scene import LightScene

pixel_pin = board.D18
num_pixels = 300
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.4, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def blink_pixel(pixel_number: int):
    pixels[pixel_number] = (255, 255, 255)
    pixels.show()
    time.sleep(.05)
    pixels[pixel_number] = (0, 0, 0)
    pixels.show()


def fill_color(r, g, b):
    pixels.fill((r, g, b))
    pixels.show()


def set_light_scene(scene: LightScene, blend=True):
    prev_rgb = pixels[scene.pixels[0]]
    print("Previous RGB: ", prev_rgb)
    new_rgb = scene.rgb
    print("New RGB: ", new_rgb)
    steps = 10  # hard code for now
    r_per_step = (new_rgb[0] - prev_rgb[0]) / steps
    g_per_step = (new_rgb[1] - prev_rgb[1]) / steps
    b_per_step = (new_rgb[2] - prev_rgb[2]) / steps
    print(f"Steps: r:{r_per_step}, g:{g_per_step}, b:{b_per_step}")
    for step in range(1, steps+1):
        for pixel in scene.pixels:
            new_r = prev_rgb[0] + step*r_per_step
            new_g = prev_rgb[1] + step*g_per_step
            new_b = prev_rgb[2] + step*b_per_step
            pixels[pixel] = (new_r, new_g, new_b)
        pixels.show()


def rainbow_cycle(wait):
    """ Sample code for cycling through the rainbow"""
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)
