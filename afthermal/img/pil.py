from PIL import Image

from ..util import from_range
from .. import hw


class ObjectConverter(object):
    def __init__(self, printer):
        self.printer = printer

    def print_out(self, obj):
        self.printer.print_image(*self.convert(obj))

    def conert(self, obj):
        raise NotImplementedError


class ImageConverter(ObjectConverter):
    def __init__(self, printer, width=hw.DOTS_PER_LINE):

        super(ImageConverter, self).__init__(printer)

        # use from range to sanity check
        from_range(8, hw.DOTS_PER_LINE+1, 8, 'width')

        self.width = width

    def open(self):
        raise NotImplementedError

    def print_file(self, fn):
        img = self.open(fn)
        self.print_out(img)


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
