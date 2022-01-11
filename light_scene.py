import json
from typing import Tuple, List


class LightScene:
    def __init__(self):
        self.rgb: Tuple = ()
        self.pixels: List[int] = []

    def to_json(self):
        return json.dumps(
            {
                'rgb': self.rgb,
                'pixels': self.pixels
            }
        )

    def from_json(self, data):
        data = json.loads(data)
        self.rgb = tuple(data['rgb'])
        self.pixels = data['pixels']
