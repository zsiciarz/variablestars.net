import unittest
import time
from unittest.mock import MagicMock, patch

from ..utils import jd_now, normalize_star_name, dict_to_observation
from stars.models import Star
from variablestars.tests.base import BaseTestCase


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


class DictToObservationTestCase(BaseTestCase):
    def setUp(self):
        super(DictToObservationTestCase, self).setUp()
        self._create_stars()
        self.row = {
            'name': self.star.name,
            'magnitude': '6.6',
            'date': str(jd_now()),
            'comp1': '65',
            'comp2': '71',
            'chart': '',
            'comment_code': '',
            'notes': 'test2',
        }

    def test_parse_row(self):
        """
        Check that succesfully parsing an input row creates an observation.
        """
        with patch.object(Star.objects, 'get') as mock_get:
            mock_get.return_value = self.star
            observation = dict_to_observation(self.row, self.observer)
        self.assertEqual(observation.observer, self.observer)
        self.assertEqual(observation.star, self.star)
        self.assertEqual(observation.notes, 'test2')
