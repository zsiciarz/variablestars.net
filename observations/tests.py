# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time

from django.test import TestCase

from mock import MagicMock, patch

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
