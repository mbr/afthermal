from afthermal.text import Text, ByteStringVisitor, Bold, Node, DoubleWidth

import pytest


@pytest.fixture
def encoding():
    return 'ascii'


@pytest.fixture
def bsv(encoding):
    return ByteStringVisitor(encoding)


def test_simple_text(bsv, encoding):
    tx = Text(u'hello, world')
    assert bsv.visit(tx) == u'hello, world'.encode(encoding)


def test_simple_formatting(bsv, encoding):
    tx = Text(u'hello')
    fmtx = Bold(tx)

    assert bsv.visit(fmtx) == (b'\x1B\x45\x01' + u'hello'.encode(encoding) +
                               b'\x1B\x45\x00')


def test_nested_formatting(bsv, encoding):
    tx = Node(Bold(Bold(Text(u'hello')), Text(u'world')), Text(u'nonbold'))

    assert bsv.visit(tx) == (
        b'\x1B\x45\x01' + u'helloworld'.encode(encoding) + b'\x1B\x45\x00' +
        'nonbold'.encode(encoding)
    )


def test_double_width(bsv, encoding):
    tx = DoubleWidth(Text(u'abc'))

    assert bsv.visit(tx) == (b'\x1D\x21\x20' + u'abc'.encode(encoding) +
                             b'\x1D\x21\x00')
