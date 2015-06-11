import json

from six import int2byte

from .port import ThrottledSerial
from .hw import get_command
from .util import from_range


class CommandAliasMixin(object):
    # printing
    def feed(self, n_dots=0):
        self.send_command('print_and_feed', n_dots)
        self.port.fed_dots(n_dots)

    # line spacing
    def set_left_margin(self, chars=None, dots=None):
        if dots is not None and chars is not None:
            raise ValueError('Can only set one of (dots, chars)')

        if dots is not None:
            # FIXME: dots seems to be not honored by printer?
            assert isinstance(dots, int)
            self.send_command('set_left_margin_dots',
                              dots / 256,
                              dots % 256)
        elif chars is not None:
            self.send_command('set_left_margin_chars',
                              chars)

    def set_line_height(self, spacing=32):
        self.send_command('set_line_spacing', spacing)
        self.port.line_height = spacing

    def set_text_align(self, alignment='L'):
        self.send_command('set_text_align', {
            'L': 0,
            'M': 1,
            'R': 2,
        }[alignment])

    # formatting
    def set_code_page(self, page):
        self.send_command('select_codepage', {
            437: 0,
            850: 1,
        }[page])

    def set_charset(self, charset='us'):
        self.send_command('select_charset', {
            'us': 0,
            'fr': 1,
            'de': 2,
            'uk': 3,
            'dk': 4,
            'se': 5,
            'it': 6,
            'es': 7,
            'jp': 8,
            'no': 9,
            'dk2': 10,
            'es2': 11,
            'latin_america': 12,
            'kr': 13,
        }[charset])

    def upload_custom_character(self, charnum, data):
        height = 3
        width = len(data) / 3

        if len(data) % 3:
            raise ValueError('Custom character must have a height of 24 dots,'
                             '(== 3 bytes).')

        if not 0 <= width <= 12:
            raise ValueError('Character must be between 0 and 12 bytes wide, '
                             'is {}.'.format(width))

        if len(data) != width * height:
            raise ValueError('Character has wrong size')  # unlikely =)

        self.write(self.CMDS['define_character'][0])

        # this should work, but doesn't. parameter order is confusing in the
        # docs, and none work, always end up a byte short
        self.write(int2byte(height))    # s
        self.write(int2byte(charnum))   # n
        self.write(int2byte(charnum))   # m (note: docs are unclear about
                                        #    ordering here, it says m, w in
                                        #    the ascii line and w, m below)
        self.write(int2byte(width))     # w

        self.write(data)

        # for some reason, we need an extra byte, but it is nowhere in the
        # specs. we'll use \x00 here, as this is pure white and not a printable
        # character
        self.write('\x00')

    def print_image(self, width, data):
        """Prints a bitmap image.

        The printer has a width of 384 dots. Each dot is a single bit.

        :param width: Width of the image, in bytes. Maximum width is 48 (= 384
                      dots).
        :param data: Must be total_dots/8 bytes long.
        """
        if len(data) % width:
            raise ValueError('Bad image format, length of data must be '
                             'divisible by width.')
        height = len(data) / width

        # send line-by-line
        for row in range(height):
            self.send_command('print_bitmap', 1, width)
            self.port.write(data[row*width:(row+1)*width], is_text=False)
            self.port.fed_dots(1)

    def clear_custom_font(self):
        self.send_command('set_user_font', 0)

    # other
    def print_test_page(self):
        self.send_command('print_test_page')
        self.port.fed_dots(28 * 32)  # 28 lines at fixed 32 dpl

    def reset(self):
        for i in range(10):
            # we run this a few times to clear data from the buffer. this
            # usually is necessary if the program crashed mid-print
            self.send_command('init')
            self.send_command('set_print_mode', 0)

    def set_density(self, density, break_time):
        self.send_command('set_printing_density',
                          chr((break_time << 5) | density))

    def set_heat(self, max_dots=64, heat_time=800, interval=20):
        self.max_dots = 64
        self.heat_time = 800
        self.interval = 20

        self.send_command(
            'set_control_parameter',
            from_range(8, 2040 + 8, 8, 'max_dots')(max_dots),
            from_range(30, 2550 + 10, 10, 'heat_time')(heat_time),
            from_range(0, 2550 + 10, 10, 'heat_interval')(interval),
        )


class ThermalPrinter(CommandAliasMixin):
    CHARS_PER_LINE = 32
    DOTS_PER_LINE = 384

    def __init__(self, port):
        self.port = port
        self.reset()

    def send_command(self, cmd, *args):
        self.write(get_command(cmd, *args))

    @classmethod
    def on_serial(cls, device='/dev/ttyAMA0', baudrate=19200):
        port = ThrottledSerial(device, baudrate)
        return cls(port)

    @classmethod
    def from_config_file(cls, fn='afthermal.conf'):
        cfg = json.load(fn)

        printer = cls.on_serial(cfg['dev'], cfg['baudrate'])
        printer.set_heat(
            max_dots=cfg['max_dots'],
            heat_time=cfg['heat_time'],
            interval=cfg['interval']
        )

        return printer

    def write(self, *args, **kwargs):
        self.port.write(*args, **kwargs)
