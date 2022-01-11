import json
import time
from typing import List, Tuple
from pymemcache.client.base import Client
import numpy
import requests
from PIL import Image
import mss.tools

from light_scene import LightScene

client = Client('localhost')
sct = mss.mss()


def get_dominant_color(im) -> Tuple:
    import numpy as np
    import scipy.cluster

    num_clusters = 5
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(numpy.product(shape[:2]), shape[2]).astype(float)
    codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)

    vectors, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
    counts, bins = numpy.histogram(vectors, len(codes))  # count occurrences

    index_max = numpy.argmax(counts)  # find most frequent
    peak = codes[index_max]
    r, g, b = list(peak)
    return int(r), int(g), int(b)


def get_quadrant_scenes() -> List[LightScene]:
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
    light_scenes: List[LightScene] = []
    # top left
    top_left_scene = LightScene()
    top_left_scene.rgb = get_dominant_color(img.resize(size=size, box=(0, 0, width, height)))
    top_left_scene.pixels = list(range(42, 70))
    light_scenes.append(top_left_scene)

    # bottom left
    bottom_left_scene = LightScene()
    bottom_left_scene.rgb = get_dominant_color(
        img.resize(size=size, box=(0, height, width, height * 2))
    )
    bottom_left_scene.pixels = list(range(70, 100))
    light_scenes.append(bottom_left_scene)

    # top right
    top_right_scene = LightScene()
    top_right_scene.rgb = get_dominant_color(
        img.resize(size=size, box=(width, 0, width * 2, height))
    )
    top_right_scene.pixels = list(range(12, 41))
    light_scenes.append(top_right_scene)

    # bottom right
    bottom_right_scene = LightScene()
    bottom_right_scene.rgb = get_dominant_color(
        img.resize(size=size, box=(width, height, width * 2, height * 2))
    )
    bottom_right_scene.pixels = list(range(0, 11)) + list(range(101, 118))
    light_scenes.append(bottom_right_scene)
    return light_scenes


if __name__ == '__main__':
    scenes: List[LightScene] = get_quadrant_scenes()
    for scene in scenes:
        requests.post('http://localhost:5000/set_scene',
                      data=scene.to_json())
