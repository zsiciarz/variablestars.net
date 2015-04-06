from unittest.mock import patch

from ..forms import BatchUploadForm
from ..utils import jd_now
from observers.models import Observer
from stars.models import Star
from variablestars.tests.base import BaseTestCase


class BatchUploadFormTestCase(BaseTestCase):
    """
    Tests for ``observations.forms.BatchUploadForm`` class.
    """
    def setUp(self):
        super(BatchUploadFormTestCase, self).setUp()
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

    def test_normalize_star_name(self):
        """
        Check that Vxxx star names are normalized to GCVS version.
        """
        form = BatchUploadForm()
        self.assertEqual(form.normalize_star_name('RR LYR'), 'RR LYR')
        self.assertEqual(form.normalize_star_name('V1339 CYG'), 'V1339 CYG')
        self.assertEqual(form.normalize_star_name('V838 MON'), 'V0838 MON')

    def test_parse_row(self):
        """
        Check that succesfully parsing an input row creates an observation.
        """
        form = BatchUploadForm()
        with patch.object(Star.objects, 'get') as mock_get:
            mock_get.return_value = self.star
            observation = form.process_row(self.row, self.observer)
        self.assertEqual(observation.observer, self.observer)
        self.assertEqual(observation.star, self.star)
        self.assertEqual(observation.notes, 'test2')
