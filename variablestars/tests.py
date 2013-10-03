# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

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
        )
