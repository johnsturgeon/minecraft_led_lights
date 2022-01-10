import time
import board
import neopixel

pixel_pin = board.D18
num_pixels = 300
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def blink_pixel(pixel_number: int):
    pixels[pixel_number] = (255, 255, 255)
    pixels.show()
    time.sleep(.05)
    pixels[pixel_number] = (0, 0, 0)
    pixels.show()

def fill_color(r, g, b):
    pixels.fill((r, g, b))
    pixels.show()