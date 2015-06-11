from PIL import Image

from . import ImageConverter


class PILImageConverter(ImageConverter):
    def open(self, fn):
        im = Image.open(fn)
        return im

    def convert(self, image):
        im = image

        # resize
        if im.size[0] > self.width:
            im = im.resize((self.width, int(float(
                self.width) * im.size[1] / im.size[0]
            )))

        # convert to B/W
        if im.mode != '1':
            im = im.convert('1')

        return (
            self.width / 8,
            b''.join(chr(ord(c) ^ 255) for c in im.tostring())
        )
