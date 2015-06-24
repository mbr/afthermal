from contextlib import contextmanager

from .hw import get_command


class Format(object):
    """Format text using printer specific escape sequences.

    :param bold: Enabled bold face.
    :param invert: Enable white-on-blasck priting.
    :param upside_down: Turn letters upside down.
    :param underline: Underline text.
    :param double_width: Print characters twice as wide.
    :param double_height: Print characters twice as high.
    :param strikethrough: Enable strikethrough.
    """
    def __init__(self, bold=False, invert=False, upside_down=False,
                 underline=False, double_width=False, double_height=False,
                 strikethrough=False):
        start = b''
        end = b''

        if strikethrough:
            # turns off all other modes, so we need to set it first
            start += get_command('set_print_mode', 1 << 6)
            end = get_command('set_print_mode', 0) + end

        if upside_down:
            start += get_command('set_updown_mode', 1)
            end = get_command('set_updown_mode', 0) + end

        if invert:
            start += get_command('set_reverse_mode', 1)
            end = get_command('set_reverse_mode', 0) + end

        if bold:
            start += get_command('set_font_bold', 1)
            end = get_command('set_font_bold', 0) + end

        if underline:
            start += get_command('set_underline', 1)
            end = get_command('set_underline', 0) + end

        enlarge = 0
        if double_width:
            enlarge |= 32
        if double_height:
            enlarge |= 1

        if enlarge:
            start += get_command('set_font_enlarge', enlarge)
            end = get_command('set_font_enlarge', 0) + end

        self.start = start
        self.end = end

    def __call__(self, buf):
        """Format text using format escape sequences."""
        return self.start + buf + self.end

    @contextmanager
    def on(self, printer):
        """Enable formatting inside context manager."""
        printer.write(self.start)
        yield
        printer.write(self.end)
