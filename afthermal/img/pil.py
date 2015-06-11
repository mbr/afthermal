from PIL import Image


class PILImageConverter(object):
    MAX_WIDTH = 384

    def from_file_name(self, fn):
        im = Image.open(fn)
        return im

    def convert(self, image):
        im = image

        # convert to B/W
        if im.mode != '1':
            im = im.convert('1')

        # resize
        if im.size[0] > self.MAX_WIDTH:
            im = im.resize(self.MAX_WIDTH, int(float(
                self.MAX_WIDTH) * im.size[1] / im.size[0]
            ))

        return b''.join(chr(ord(c) ^ 255) for c in im.tostring())
