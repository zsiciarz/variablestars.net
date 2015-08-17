import unittest
import time
from unittest.mock import MagicMock, patch

from ..utils import jd_now, normalize_star_name


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


class NormalizeStarNameTestCase(unittest.TestCase):
    def test_normalize_star_name(self):
        """
        Check that Vxxx star names are normalized to GCVS version.
        """
        self.assertEqual(normalize_star_name('RR LYR'), 'RR LYR')
        self.assertEqual(normalize_star_name('V1339 CYG'), 'V1339 CYG')
        self.assertEqual(normalize_star_name('V838 MON'), 'V0838 MON')
