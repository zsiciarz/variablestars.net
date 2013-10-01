# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Observation
from stars.models import Star, VariabilityType


class ObservationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'stargazer',
            'stargazer@example.com',
            '123456',
        )
        self.observer = self.user.observer
        self.observer.aavso_code = 'XYZ'
        self.observer.save()
        self.variability_type = VariabilityType.objects.create(
            code='M',
            long_description='Mira stars',
        )
        self.star = Star.objects.create(
            constellation='LEO',
            name='R LEO',
            ra='09:47:33.5',
            dec='+11:25:44',
            variability_type=self.variability_type,
            max_magnitude=4.4,
            min_magnitude=11.3,
        )

    """
    Tests for Observation model.
    """
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
