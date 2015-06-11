from . import ObjectConverter


class QRCodeConverter(ObjectConverter):
    def __init__(self, printer, invert=False):
        super(QRCodeConverter, self).__init__(printer)
        self.invert = invert

    def convert(self, code):
        output = []
        size = None
        tbl = ({'0': b'\xFF', '1': b'\x00'} if self.invert else
               {'1': b'\xFF', '0': b'\x00'})

        for line in code.text().splitlines():
            outline = []
            for c in line:
                outline.append(tbl[c])

            l = b''.join(outline)
            for i in range(8):
                # 8x8 pixels
                output.append(l)

        size = len(output[0])
        return size, b''.join(output)
