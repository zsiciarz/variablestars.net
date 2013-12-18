# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..models import Observer
from observations.models import Observation
from variablestars.tests.base import BaseTestCase


class ObserverModelTestCase(BaseTestCase):
    """
    Tests for Observer model.
    """

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

    def test_recent_observations(self):
        observations = self.observer.recent_observations()
        self.assertEqual(observations[0].star, self.star)
        observations = self.observer2.recent_observations()
        self.assertEqual(observations[0].star, self.periodic_star)

    def test_observed_star_count(self):
        self.assertEqual(self.observer.observed_stars_count(), 2)


class ObserverQuerySetTestCase(ObserverModelTestCase):
    """
    Tests for ObserverQuerySet class (accessed through a manager).
    """

    def test_observations_count(self):
        """
        Check that returned Observer instances have are annotated with
        number of observations.
        """
        observers = Observer.objects.with_observations_count().order_by('pk')
        self.assertEqual(observers[0], self.observer)
        observations_count = Observation.objects.filter(
            observer=self.observer
        ).count()
        self.assertEqual(observers[0].observations_count, observations_count)

    def test_total_stats(self):
        stats = Observer.objects.get_total_stats()
        self.assertEqual(stats['total_observer_count'], 2)
