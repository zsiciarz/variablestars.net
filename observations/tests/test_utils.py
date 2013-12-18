# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import time

from mock import MagicMock, patch

from ..utils import jd_now


class JdNowTestCase(unittest.TestCase):
    """
    Tests for ``observations.utils.jd_now`` function.
    """
    def test_unix_epoch_jd(self):
        """
        Check JD value at the beggining of Unix epoch.
        """
        mock_time = MagicMock()
        mock_time.return_value = 0.0
        with patch.object(time, 'time', mock_time):
            jd = jd_now()
            self.assertEqual(jd, 2440587.5)
