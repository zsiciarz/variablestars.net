# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from observations.models import Observation
from variablestars.tests import BaseTestCase


class ObserverModelTestCase(BaseTestCase):
    """
    Tests for Observer model.
    """

    def setUp(self):
        super(ObserverModelTestCase, self).setUp()
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
                jd=2456567.2550 + i,
                magnitude=6.5 - 0.2 * i,
            )

    def test_str(self):
        """
        String representation of an observer is his username (sometimes with
        full name).
        """
        self.assertEqual(str(self.observer), self.user.username)
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.assertEqual(str(self.observer), 'stargazer (John Doe)')

    def test_top_stars(self):
        expected = [
            {'star_id': self.star.id, 'star__name': self.star.name, 'observations_count': 10},
            {'star_id': self.periodic_star.id, 'star__name': self.periodic_star.name, 'observations_count': 5},
        ]
        top_stars = list(self.observer.top_stars())
        self.assertEqual(top_stars, expected)

    def test_observed_star_count(self):
        self.assertEqual(self.observer.observed_stars_count(), 2)
