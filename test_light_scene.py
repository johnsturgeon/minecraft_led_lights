import pytest
from light_scene import LightScene


def test_to_from_json():
    scene1 = LightScene()
    scene1.rgb = (1, 2, 3)
    scene1.pixels = [4, 5, 6]
    assert scene1.to_json() == '{"rgb": [1, 2, 3], "pixels": [4, 5, 6]}'

    scene2 = LightScene()
    scene2.from_json(scene1.to_json())
    assert scene2.rgb == (1, 2, 3)
    assert scene2.pixels == [4, 5, 6]