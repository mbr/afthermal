from six import int2byte


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


def get_command(cmd, *args):
    seq, nargs = CMDS[cmd]

    if not len(args) == nargs:
        raise ValueError('Invalid argument count for {}, needs {}'.format(
            cmd, nargs)
        )

    buf = [seq]
    buf.extend(int2byte(i) for i in args)

    return b''.join(buf)
