#############################################################################################################
###
### Conversions to human readable
###
#############################################################################################################

import math


def human_readable_number(x, digits=3):
    """
    Rounds a number to a fixed number of significant digits.
    """
    if not isinstance(x, int) and not isinstance(x, float):
        return x
    if digits <= 0:
        return x
    if x == 0 or not math.isfinite(x):
        return x

    magnitude = int(math.floor(math.log10(abs(x)))) + 1

    # kein round verwenden, das funktioniert nicht!
    if magnitude >= digits:
        if x >= 0:
            result = math.floor(x / 10**(magnitude-digits)+0.5) * 10**(magnitude-digits)
        else:
            result = math.ceil(x / 10**(magnitude-digits)-0.5) * 10**(magnitude-digits)
    else:
        factor = 10**(digits - magnitude)
        if x >= 0:
            result = math.floor(x * factor + 0.5) / factor
        else:
            result = math.ceil(x * factor - 0.5) / factor

    if math.modf(result)[0] == 0:
        return int(result)
    return result


def human_readable_number_1(x):
    return human_readable_number(x, digits=1)


def human_readable_number_2(x):
    return human_readable_number(x, digits=2)


def human_readable_number_3(x):
    return human_readable_number(x, digits=3)


def human_readable_number_4(x):
    return human_readable_number(x, digits=4)


def human_readable_seconds(seconds):
    """Converts seconds to human readable time"""
    TIME_DURATION_UNITS = (
        ("week", 60 * 60 * 24 * 7),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("min", 60),
        ("sec", 1),
    )

    if seconds < 60:
        return str(round(seconds, 1)) + " secs"
    parts = []
    seconds = round(seconds, 0)
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


def human_readable_bytes(num, suffix="B"):
    """Converts Bytes to human readable size"""
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, "Y", suffix)