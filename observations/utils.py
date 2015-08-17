import time


def jd_now():
    """
    Returns Julian Date at the current moment.
    """
    return 2440587.5 + time.time() / 86400.0


def normalize_star_name(name):
    """
    Normalize star name with GCVS names, for example: V339 -> V0339.
    """
    digits = '123456789'
    if name[0] == 'V' and name[1] in digits and name[4] not in digits:
        name = 'V0' + name[1:]
    return name
