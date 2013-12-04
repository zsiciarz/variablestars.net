# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from djet.assertions import InstanceAssertionsMixin
from djet.files import create_inmemory_file
from mock import MagicMock, patch

from .forms import BatchUploadForm
from .models import Observation
from .utils import jd_now
from stars.models import Star
from variablestars.tests import BaseTestCase


class ObservationModelTestCase(BaseTestCase):
    """
    Tests for Observation model.
    """

    def test_str(self):
        """
        Check for string representation of an observation.
        """
        observation = Observation(
            observer=self.observer,
            star=self.star,
            jd=2456567.2550,
            magnitude=8.5,
        )
        expected = "%s %s %s" % (
            observation.star, observation.jd, observation.magnitude,
        )
        self.assertEqual(str(observation), expected)

    def test_update_star_observations_count(self):
        """
        Check that creating new observations updates star's observations_count
        denormalized field.
        """
        self.assertEqual(self.star.observations_count, 10)
        observation = Observation.objects.create(
            observer=self.observer,
            star=self.star,
            jd=2456567.2550,
            magnitude=8.5,
        )
        star = Star.objects.get(pk=self.star.pk)
        self.assertEqual(star.observations_count, 11)
        observation.delete()
        star = Star.objects.get(pk=self.star.pk)
        self.assertEqual(star.observations_count, 10)


class ObservationManagerTestCase(BaseTestCase):
    def test_top_stars(self):
        expected = [
            {'star_id': self.star.id, 'star__name': self.star.name, 'observations_count': 10},
            {'star_id': self.periodic_star.id, 'star__name': self.periodic_star.name, 'observations_count': 8},
        ]
        top_stars = list(Observation.objects.top_stars())
        self.assertEqual(top_stars, expected)

    def test_top_observers(self):
        """
        Check that top_observers() returns a list of people ordered by
        the number of observations.
        """
        expected = [
            {
                'observer_id': self.observer.id,
                'observer__aavso_code': self.observer.aavso_code,
                'observations_count': 15,
            },
            {
                'observer_id': self.observer2.id,
                'observer__aavso_code': self.observer2.aavso_code,
                'observations_count': 3,
            },
        ]
        top_observers = list(Observation.objects.top_observers())
        self.assertEqual(top_observers, expected)

    def test_recent_observations(self):
        observations = Observation.objects.recent_observations()
        self.assertEqual(observations[0].observer, self.observer)


class JdNowTestCase(TestCase):
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


class BatchUploadFormTestCase(InstanceAssertionsMixin, BaseTestCase):
    def setUp(self):
        super(BatchUploadFormTestCase, self).setUp()
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
        form = BatchUploadForm()
        self.assertEqual(form.normalize_star_name('RR LYR'), 'RR LYR')
        self.assertEqual(form.normalize_star_name('V1339 CYG'), 'V1339 CYG')
        self.assertEqual(form.normalize_star_name('V838 MON'), 'V0838 MON')

    def test_parse_row(self):
        form = BatchUploadForm()
        with self.assert_instance_created(Observation, star=self.star, notes='test2'):
            form.process_row(self.row, self.observer)


class UploadObservationsViewTestCase(InstanceAssertionsMixin, BaseTestCase):
    def setUp(self):
        super(UploadObservationsViewTestCase, self).setUp()
        self.url = reverse('observations:upload_observations')
        self.client.login_observer()
        self.lines = [
            "#TYPE=VISUAL",
            "#OBSCODE=%s" % self.observer.aavso_code,
            "#SOFTWARE=variablestars.net",
            "#DELIM=,",
            "#DATE=JD",
            "#OBSTYPE=Visual",
            "%s,2450702.1234,<11.1,na,110,113,070613,test3" % self.star.name,
        ]

    def test_response(self):
        response = self.client.get(self.url)
        self.assertContains(response, _("Upload observations"))
        self.assertTemplateUsed(response, "observations/upload_observations.html")

    def test_no_file(self):
        response = self.client.post(self.url, {
            'aavso_file': '',
        })
        self.assertFormError(response, 'form', 'aavso_file', _("This field is required."))

    def test_correct_file(self):
        aavso_file = create_inmemory_file('data.txt', "\n".join(self.lines))
        with self.assert_instance_created(Observation, star=self.star, notes='test3'):
            response = self.client.post(self.url, {
                'aavso_file': aavso_file,
            }, follow=True)
            self.assertContains(response, _("File uploaded successfully!"))

    def test_malformed_file(self):
        """
        Check that a bad magnitude value raises an exception.
        """
        observations_count_before = Observation.objects.count()
        self.lines[-1] = "%s,2450702.1234,ASDF,na,110,113,070613,test3" % self.star.name
        aavso_file = create_inmemory_file('data.txt', "\n".join(self.lines))
        response = self.client.post(self.url, {
            'aavso_file': aavso_file,
        }, follow=True)
        self.assertContains(response, _("File uploaded successfully!"))
        observations_count_after = Observation.objects.count()
        self.assertEqual(observations_count_after, observations_count_before)
