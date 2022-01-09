from typing import List
import pyglet
from pyglet import shapes
from pymemcache.client.base import Client
import time
import numpy
from PIL import ImageGrab, Image
from mss.darwin import MSS as mss
import mss.tools
from colorthief import ColorThief
IS_DRAWING = False
client = Client('localhost')
sct = mss.mss()


def get_dominant_color(im) -> []:
    import numpy as np
    import scipy.cluster

    num_clusters = 5
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(numpy.product(shape[:2]), shape[2]).astype(float)

    # print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)
    # print('cluster centres:\n', codes)

    vectors, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = numpy.histogram(vectors, len(codes))    # count occurrences

    index_max = numpy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    return list(peak)


def draw(dt):
    print(dt)
    global sct
    left, top, width, height = client.get('front_window_frame').decode().split(',')
    left = int(left)
    top = int(top)
    width = int(width)
    height = int(height)

    monitor = {"top": top, "left": left, "width": width, "height": height}
    sct_img = sct.grab(monitor)
    # Convert to PIL/Pillow Image
    img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    size = (75, 75)
    image_quadrants: List = []
    circles: List[shapes.Circle] = []
    # crop left, upper, right, lower
    # top left
    image_quadrants.append(img.resize(size=size, box=(0, 0, width, height)))
    # bottom left
    image_quadrants.append(img.resize(size=size, box=(0, height, width, height*2)))
    # top right
    image_quadrants.append(img.resize(size=size, box=(width, 0, width*2, height)))
    # bottom right
    image_quadrants.append(img.resize(size=size, box=(width, height, width*2, height*2)))
    batch = pyglet.graphics.Batch()
    for image in image_quadrants:
        r, g, b = get_dominant_color(image)
        rgb = (int(r), int(g), int(b))
        x, y = coordinates_for_index(image_quadrants.index(image))
        radius = 50
        circles.append(shapes.Circle(x, y, radius, color=rgb, batch=batch))
    window.clear()
    batch.draw()


def coordinates_for_index(index: int):
    if index == 0:
        return 50, 200
    if index == 1:
        return 50, 50
    if index == 2:
        return 200, 200
    if index == 3:
        return 200, 50


if __name__ == '__main__':
    w_width = 250
    w_height = 250
    window = pyglet.window.Window(w_width, w_height)
    pyglet.clock.schedule_interval(draw, 1/60.0)
    # run the pyglet application
    pyglet.app.run()

    # pixels = Adafruit_NeoPixel(300, 6, "NEO_GRB + NEO_KHZ800")
    # effects = NeoPixel_Effects(pixels)
    # pixels.begin()
    #
    # pixels.clear()
    # img = ImageGrab.grab(bbox=(900, 900, 4000, 2300))
    # img.show()
    # r, g, b, _ = get_dominant_color(img)
    # pixels.fill(color=pixels.Color(r, g, b), start=0, count=300)
    # pixels.show()
    #
