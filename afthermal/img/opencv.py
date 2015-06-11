import cv2
import numpy as np

from . import ImageConverter


class OpenCVImageConverter(ImageConverter):
    def __init__(self, printer, width=None, bw_conv='bin_threshold'):
        super(OpenCVImageConverter, self).__init__(printer, width)
        self.bw_conv = bw_conv

    def open(self, fn):
        return cv2.imread(fn)

    def convert(self, image):
        img = image

        # resize
        if len(img.shape) > 2:
            h, w, color = img.shape
        else:
            h, w = img.shape
            color = False

        if len(img) > self.width:
            img = cv2.resize(img, (self.width, int(float(self.width) * h / w)))

        # convert to grayscale
        if color:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # convert to B/W
        if np.amax(img) != 1:
            # pass
            if self.bw_conv == 'bin_threshold':
                img = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)[1]
            else:
                raise ValueError('Unknown conversion method: {}'.format(
                    self.bw_conv
                ))

        # pack into bitstring and then invert
        packed = np.invert(np.packbits(img))
        return self.width / 8, packed.tostring()
