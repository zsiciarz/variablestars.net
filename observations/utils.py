# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time


def jd_now():
    """
    Returns Julian Date at the current moment.
    """
    return 2440587.5 + time.time() / 86400.0
