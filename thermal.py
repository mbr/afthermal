import time

from serial import Serial
from six import int2byte


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
        self.send_command('init')
        self.send_command('set_print_mode', 0)

    def set_density(self, density, break_time):
        self.send_command('set_printing_density',
                          chr((break_time << 5) | density))

    def set_heat(self, max_dots=7, heat_time=80, interval=2):
        self.send_command('set_control_parameter',
                          max_dots,
                          heat_time,
                          interval)


class ThrottledSerial(Serial):
    dot_feed_time = 0.0625       # time required to write one image dot
    line_feed_time = 32 * 0.005  # time required to print one line
    write_ready = 0

    def wait_for_write(self):
        # ensure we're not writing lines too fast
        now = time.time()
        if now < self.write_ready:
            time.sleep(self.write_ready - now)

    def fed_lines(self, n_lines=1):
        now = time.time()
        self.write_ready = now + n_lines * self.line_feed_time

    def fed_dots(self, n_dots):
        now = time.time()
        self.write_ready = now + n_dots * self.dot_feed_time

    def write(self, data, is_text=True):
        def wr(*args, **kwargs):
            self.wait_for_write()
            super(ThrottledSerial, self).write(*args, **kwargs)

        if not is_text:
            wr(data)
            return

        while data:
            nl_idx = data.find(b'\n')
            if nl_idx == - 1:
                # no newline, just write
                wr(data)
                break

            nl_idx += 1  # include newline

            chunk, data = data[:nl_idx], data[nl_idx:]
            wr(chunk)
            self.fed_lines(1)


class Format(object):
    def __init__(self, bold=False, invert=False, upside_down=False,
                 underline=False, double_width=False, double_height=False,
                 strikethrough=False):
        start = b''
        end = b''

        if strikethrough:
            # turns off all other modes, so we need to set it first
            start += ThermalPrinter.get_command('set_print_mode', 1 << 6)
            end = ThermalPrinter.get_command('set_print_mode', 0) + end

        if upside_down:
            start += ThermalPrinter.get_command('set_updown_mode', 1)
            end = ThermalPrinter.get_command('set_updown_mode', 0) + end

        if invert:
            start += ThermalPrinter.get_command('set_reverse_mode', 1)
            end = ThermalPrinter.get_command('set_reverse_mode', 0) + end

        if bold:
            start += ThermalPrinter.get_command('set_font_bold', 1)
            end = ThermalPrinter.get_command('set_font_bold', 0) + end

        if underline:
            start += ThermalPrinter.get_command('set_underline', 1)
            end = ThermalPrinter.get_command('set_underline', 0) + end

        enlarge = 0
        if double_width:
            enlarge |= 32
        if double_height:
            enlarge |= 1

        if enlarge:
            start += ThermalPrinter.get_command('set_font_enlarge', enlarge)
            end = ThermalPrinter.get_command('set_font_enlarge', 0) + end

        self.start = start
        self.end = end

    def __call__(self, buf):
        return self.start + buf + self.end


class ThermalPrinter(CommandAliasMixin):
    # commands are in the form of (sequence, number of arguments)
    CMDS = {
        # PRINT COMMAND
        # LF         Print and line feed: See "Print and Feed n lines"
        # HT         JMP to the TAB position: not implemented
        # FF         Print the data in the buffer: not implemented
        # ESC FF     Print the data in the buffer: not implemented
        # ESC J      Print and Feed n dots paper
        'print_and_feed': (b'\x1B\x4A', 1),
        # ESC d      Print and Feed n lines
        'print_and_linefeed': (b'\x1B\x64', 1),
        # ESC =      Toggle the printer online or offline
        # FIXME: What does this *do* ?
        'set_online': (b'\x1B\x3D', 1),

        # LINE SPACING COMMAND
        # ESC 2      Set line spacing to default value (32)
        # ESC 3 n    Set line spacing to n dots
        'set_line_spacing': (b'\x1B\x33', 1),
        # ESC a n    Set align mode
        'set_text_align': (b'\x1B\x61', 1),
        # GS L nL nH Set the left blank margin with dots
        'set_left_margin_dots': (b'\x1B\x24', 2),
        # ESC B n    Set the left blank char number
        'set_left_margin_chars': (b'\x1B\x42', 1),

        # CHARACTER COMMAND
        # ESC ! n    Select print mode(s)
        'set_print_mode': (b'\x1B\x21', 1),
        # GS ! n     Set or Cancel the double with and height
        'set_font_enlarge': (b'\x1D\x21', 1),
        # ESC E n    Set or Cancel bold font
        'set_font_bold': (b'\x1B\x45', 1),
        # ESC SP     Set the space between chars
        # FIXME: manual is broken here?
        # ESC S0     Turn double width on
        'enable_double_width': (b'\x1B\x0E', 0),
        # ESC DC4    Turn double width off
        'disable_double_width': (b'\x1B\x14', 0),
        # ESC { n    Turn upside-down printing mode on/off
        'set_updown_mode': (b'\x1B\x7B', 1),
        # GS B n     Turn inverting printing mode on/off
        'set_reverse_mode': (b'\x1D\x42', 1),
        # ESC - n    Set the underline dots(0,1,2)
        'set_underline': (b'\x1B\x2D', 1),
        # ESC % n    Select/Cancel user-defined characters
        'set_user_font': (b'\x1B\x25', 1),
        # ESC &      Define user-defined characters
        'define_character': (b'\x1B\x26', -1),
        # ESC R n    Select an internal character set
        'select_charset': (b'\x1B\x52', 1),
        # EST t n    Select character code table
        'select_codepage': (b'\x1B\x74', 1),

        # BIT IMAGE COMMAND
        # all the image commands seem a bit crappy, print_bitmap seems to work
        # good enough to supercede all the others
        # ESC *      Select bit-image mode
        # GS /       Print downloaded bit image
        # # GS *       Define downloaded bit image
        # GS v       Print bitmp with width and height
        # DC2 *      Print the bitmap
        'print_bitmap': (b'\x12\x2A', 2),
        # DC2 V      Print MSB bitmap
        # DC2 v      Print LSB bitmap

        # BOARD PARA COMMAND
        'print_test_page': (b'\x12\x54', 0),

        # not implemented: jump_tab                 # pg. 10
        # not implemented: jump_tab                 # pg. 10
        # not implemented: jump_tab                 # pg. 10
        'init': (b'\x1B\x40', 0),                   # pg. 19
        'set_control_parameter': (b'\x1B\x37', 3),  # pg. 23
        'set_printing_density': (b'\x12\x23', 2),   # pg. 23
    }

    def __init__(self, port):
        self.port = port
        self.reset()

    @classmethod
    def get_command(cls, cmd, *args):
        seq, nargs = cls.CMDS[cmd]

        if not len(args) == nargs:
            raise ValueError('Invalid argument count for {}, needs {}'.format(
                cmd, nargs)
            )

        buf = [seq]
        buf.extend(int2byte(i) for i in args)

        return b''.join(buf)

    def send_command(self, cmd, *args):
        self.write(self.get_command(cmd, *args))

    @classmethod
    def on_serial(cls, device='/dev/ttyAMA0', baudrate=19200):
        port = ThrottledSerial(device, baudrate)
        return cls(port)

    def write(self, *args, **kwargs):
        self.port.write(*args, **kwargs)
