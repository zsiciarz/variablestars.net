# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

from observations.models import Observation
from stars.models import Star, VariabilityType


class BaseTestCase(TestCase):
    """
    Base test class for other test cases to derive from.
    """

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
            period=None,
            epoch=None,
        )
        self.periodic_star = Star.objects.create(
            constellation='CEP',
            name='T CEP',
            ra='21:09:31.8',
            dec='+68:29:27',
            variability_type=self.variability_type,
            max_magnitude=5.2,
            min_magnitude=11.3,
            period=388.14,
            epoch=2444177.0,
        )
        for i in range(10):
            Observation.objects.create(
                observer=self.observer,
                star=self.star,
                jd=2456567.2550 + i,
                magnitude=8.5 + 0.1 * i,
            )
        for i in range(5):
            Observation.objects.create(
                observer=self.observer,
                star=self.periodic_star,
                jd=2456587.2550 + i,
                magnitude=6.5 - 0.2 * i,
            )
