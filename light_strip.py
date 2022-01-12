import time
from threading import Thread

import board
import neopixel
import colorsys
from anim_overrides import MySparkle
from light_scene import LightScene
from rain import Rain
from math import isclose

pixel_pin = board.D18
num_pixels = 300
default_brightness = 0.5
ORDER = neopixel.GRB
IS_RAINING = False

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=default_brightness, auto_write=False, pixel_order=ORDER
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


def raining():
    global IS_RAINING
    IS_RAINING = True
    my_rain = Rain(pixels)
    while IS_RAINING:
        my_rain.animate()

def stop_rain():
    global IS_RAINING
    IS_RAINING = False

def blend_to_color(new_rgb, steps: int, speed: float):
    prev_rgb = pixels[0]
    r_per_step = (new_rgb[0] - prev_rgb[0]) / steps
    g_per_step = (new_rgb[1] - prev_rgb[1]) / steps
    b_per_step = (new_rgb[2] - prev_rgb[2]) / steps
    for step in range(1, steps+1):
        new_r = prev_rgb[0] + int(step*r_per_step)
        new_g = prev_rgb[1] + int(step*g_per_step)
        new_b = prev_rgb[2] + int(step*b_per_step)
        pixels.fill((new_r, new_g, new_b))
        time.sleep(speed)
        pixels.show()

def rainbow_cycle(wait):
    """ Sample code for cycling through the rainbow"""
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def set_brightness(brightness: float, animate: bool=True):
    if not animate:
        pixels.brightness = brightness
        return
    steps: int = 12
    step_delta: float = (pixels.brightness - brightness) / steps
    while not isclose(pixels.brightness, brightness):
        pixels.brightness = pixels.brightness - step_delta
        pixels.show()
        time.sleep(1/steps)
    print("done")

def sunset(phase: int):
    sunset_color = (40, 8, 0)
    set_brightness(0)
    if IS_RAINING:
        stop_rain()
        time.sleep(0.1)
    pixels.fill(sunset_color)
    pixels.show()
    set_brightness(default_brightness)

# if __name__ == '__main__':
#     thread = Thread(target=raining)
#     thread.start()
#     set_brightness(0)
#     set_brightness(0.5)
