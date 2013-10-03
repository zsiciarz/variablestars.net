# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .models import Observation
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
        self.assertEqual(self.star.observations_count, 0)
        observation = Observation.objects.create(
            observer=self.observer,
            star=self.star,
            jd=2456567.2550,
            magnitude=8.5,
        )
        star = Star.objects.get(pk=self.star.pk)
        self.assertEqual(star.observations_count, 1)
        observation.delete()
        star = Star.objects.get(pk=self.star.pk)
        self.assertEqual(star.observations_count, 0)
