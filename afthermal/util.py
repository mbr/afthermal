def in_range(low, high, step=None):
    def check(value):
        if not low <= value < high:
            return False

        if step is not None:
            return (value - low) % step == 0
        return True

    return check


def from_range(low, high, step=None, value_name='value'):
    def convert(value):
        if not in_range(low, high, step)(value):
            msg = '{} not in range: {}; must be {} <= {} < {}'.format(
                value_name, value, low, value_name, high
            )

            if step is not None:
                msg += ' in steps of {}'.format(step)
            raise ValueError(msg)

        if step is not None:
            return (value - low) / step
        return value - low
    return convert
