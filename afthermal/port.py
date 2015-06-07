import time

from serial import Serial


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
