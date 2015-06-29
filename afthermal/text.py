from collections import Counter
from contextlib import contextmanager

from .hw import get_command


# use HTML-like for text?
#
# <b>: bold
# <inv>: invert
# <updown>: upside down
# <u>: underline
# <dw>: double width
# <dh>: double height
# <del>: strike through


class Visitor(object):
    def visit(self, node):
        for cls in type(node).mro():
            meth = getattr(self, 'visit_' + cls.__name__, None)
            if meth is None:
                continue
            return meth(node)

        raise NotImplementedError('No visitation method visitor for {}'
                                  .format(node.__class__.__name__))


class FormattingState(Counter):
    def enable_seq(self, seq):
        self[seq] += 1
        if self[seq] == 1:
            return seq

        return b''

    def disable_seq(self, seq, off_seq):
        self[seq] -= 1
        if not self[seq]:
            return off_seq

        return b''

    @contextmanager
    def enabled(self, buf, seq, off_seq):
        buf.append(self.enable_seq(seq))
        yield
        buf.append(self.disable_seq(seq, off_seq))


class Node(object):
    def __init__(self, *children):
        self.children = children


class ByteStringVisitor(Visitor):
    def __init__(self, encoding='ascii'):
        super(ByteStringVisitor, self).__init__()
        self.encoding = encoding
        self.formats = FormattingState()
        self.enlarge = FormattingState()

    def visit_FormatMode(self, node):
        buf = []

        # if we're not in the correct mode, activate
        with self.formats.enabled(buf, node.SEQ_ON, node.SEQ_OFF):
            for child in node.children:
                buf.append(self.visit(child))

        return b''.join(buf)

    def visit_EnlargeMode(self, node):
        buf = []

        # if we're not in the correct mode, activate
        with self.formats.enabled(
            buf,
            get_command('set_font_enlarge', node.FLAG),
            get_command('set_font_enlarge', 0)
        ):
            for child in node.children:
                buf.append(self.visit(child))

        return b''.join(buf)

    def visit_Text(self, node):
        # FIXME: escape special chars
        return node.text.encode(self.encoding)

    def visit_Node(self, node):
        return b''.join(map(self.visit, node.children))


class FormatMode(Node):
    pass


class EnlargeMode(Node):
    pass


class Text(object):
    def __init__(self, text):
        self.text = text


class UpsideDown(FormatMode):
    SEQ_ON = get_command('set_updown_mode', 1)
    SEQ_OFF = get_command('set_updown_mode', 0)


class Invert(FormatMode):
    SEQ_ON = get_command('set_reverse_mode', 1)
    SEQ_OFF = get_command('set_reverse_mode', 0)


class Bold(FormatMode):
    SEQ_ON = get_command('set_font_bold', 1)
    SEQ_OFF = get_command('set_font_bold', 0)


class Underline(FormatMode):
    SEQ_ON = get_command('set_underline', 1)
    SEQ_OFF = get_command('set_underline', 0)


class Strikethrough(FormatMode):
    SEQ_ON = get_command('set_print_mode', 1 << 6)
    SEQ_ON = get_command('set_print_mode', 0)


class DoubleWidth(EnlargeMode):
    FLAG = 32


class DoubleHeight(EnlargeMode):
    FLAG = 1
