from PIL import Image


from . import ImageConverter


class PILImageConverter(ImageConverter):
    def open(self, fn):
        im = Image.open(fn)
        return im

    def convert(self, image):
        im = image
        width = self.printer.width

        # resize
        if im.size[0] > width:
            im = im.resize((width, int(float(
                width) * im.size[1] / im.size[0]
            )))

        # convert to B/W
        if im.mode != '1':
            im = im.convert('1')

        return (
            width / 8,
            b''.join(chr(ord(c) ^ 255) for c in im.tostring())
        )
