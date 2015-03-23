import time


def jd_now():
    """
    Returns Julian Date at the current moment.
    """
    return 2440587.5 + time.time() / 86400.0
