import time

from serial import Serial


class ThrottledSerial(Serial):
    """A throttled serial port implementation.

    For use with printer devices that have no flow control. Counts how many
    lines/dots were sent and based on a speed estimate of the printer's paper
    feed speed, throttles writes accordingly.
    """
    # FIXME: these need to get attached to a printer
    dot_feed_time = 0.0625       # time required to write one image dot
    line_feed_time = 32 * 0.005  # time required to print one line
    write_ready = 0

    def wait_for_write(self):
        """Wait until the printer is safe to write to."""
        # ensure we're not writing lines too fast
        now = time.time()
        if now < self.write_ready:
            time.sleep(self.write_ready - now)

    def fed_lines(self, n_lines=1):
        """Notify that lines of characters have been written.

        :param n_lines: Number of lines written.
        """
        now = time.time()
        self.write_ready = now + n_lines * self.line_feed_time

    def fed_dots(self, n_dots):
        """Notify that lines of dots have been written.

        :param n_dots: The number of vertical dots that have been fed.
        """
        now = time.time()
        self.write_ready = now + n_dots * self.dot_feed_time

    def write(self, data, is_text=True):
        # FIXME: the printer itself should probably emit events
        # FIXME: should also count normal characters for line-count
        """Count and write data.

        Waits for write, then passes on data. Can count text data if necessary.

        :param data: Data to write.
        :param is_text: If true, assume the data is text and assumes a new line
                        is fed if ``\n`` is encountered.
        """
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
