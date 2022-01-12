from adafruit_led_animation.animation.sparkle import Sparkle


class MySparkle(Sparkle):

    def draw(self):
        self._pixels = [self._random_in_mask() for _ in range(self._num_sparkles)]
        for pixel in self._pixels:
            self.pixel_object[pixel] = self._sparkle_color

    def after_draw(self):
        self.show()
        for pixel in self._pixels:
            self.pixel_object[pixel % self._num_pixels] = self._half_color
            if (pixel + 1) % self._num_pixels in self._mask:
                self.pixel_object[(pixel + 1) % self._num_pixels] = self._dim_color


    def _set_color(self, color):
        half_color = tuple(color[rgb] // 20 for rgb in range(len(color)))
        dim_color = tuple(color[rgb] // 10 for rgb in range(len(color)))
        for pixel in range(  # pylint: disable=consider-using-enumerate
                len(self.pixel_object)
        ):
            if self.pixel_object[pixel] == self._half_color:
                self.pixel_object[pixel] = half_color
            elif self.pixel_object[pixel] == self._dim_color:
                self.pixel_object[pixel] = dim_color
        self._half_color = half_color
        self._dim_color = dim_color
        self._sparkle_color = color
