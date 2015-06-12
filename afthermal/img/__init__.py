import os

from ..util import from_range

# can't ship without lena!
LENA_FN = os.path.join(os.path.dirname(__file__), 'lena30.jpg')


class ObjectConverter(object):
    """Converts objects into bitmap data suitable for sending to the printer.

    :param printer: Printer to send data to when printing is requested.
    """
    def __init__(self, printer):
        self.printer = printer

    def print_out(self, obj):
        """Print object.

        :param obj: An object to print.
        """
        self.printer.print_image(*self.convert(obj))

    def convert(self, obj):
        """Convert an object into printable bitmap.

        :param obj: Object to convert.
        :return: A tuple suitable for passing to
                 :meth:`.ThermalPrinter.print_image`.
        """
        raise NotImplementedError


class ImageConverter(ObjectConverter):
    """Converts images to bitmap data suitable for printing.

    :param printer: A :class:`.ThermalPrinter` instance.
    :param width: Number of dots to print picture with (width). Defaults to
                  the maximum width of the printer.
    """
    def __init__(self, printer, width=None):
        super(ImageConverter, self).__init__(printer)

        if width is None:
            width = printer.DOTS_PER_LINE

        self.width = width

        # use from range to sanity check
        from_range(8, printer.DOTS_PER_LINE+1, 8, 'width')

    def open(self, fn):
        """Open image.

        :param fn: Filename to open.
        :return: An image object, suitable for passing to convert.
        """
        raise NotImplementedError

    def print_file(self, fn):
        """Prints a file directly.

        :param fn: Filename to open.
        """
        img = self.open(fn)
        self.print_out(img)
