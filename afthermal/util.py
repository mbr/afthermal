def in_range(low, high, step=None):
    """Create a function that checks whether or not a value is in range.

    :param low: Minimum valid value; value must be ``>= low``
    :param high: Smallest invalid value; value must be ``< high``
    :param step: Step size. Value must be a multipe of ``

    :return: A function returning a boolean indicating whether or not the
    value is valid, that is in the specified range and satisfying ``val = low +
    k * step`` for an integer ``k``.
    """
    def check(value):
        if not low <= value < high:
            return False

        if step is not None:
            return (value - low) % step == 0
        return True

    return check


def from_range(low, high, step=None, value_name='value'):
    """Normalizes a value.

    Will first check if the value is in range. If not, raises a
    ``~exceptions.ValueError``.

    :param low: See :func:`.in_range`.
    :param high: See :func:`.in_range`.
    :param step: See :func:`.in_range`.
    :param value_name: Name for the value. Use in exception error message.
    :return: ``(val - low) [/ step]``. Division by step only if step is not
             ``None``.
    """
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
