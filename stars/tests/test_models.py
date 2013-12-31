# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..models import Star
from variablestars.tests.base import BaseTestCase


class StarQuerySetTestCase(BaseTestCase):
    """
    Tests for ``StarQuerySet`` class.
    """
    def setUp(self):
        super(StarQuerySetTestCase, self).setUp()
        self._create_stars()
        self._create_observations()

    def test_total_stats(self):
        stats = Star.objects.get_total_stats()
        self.assertEqual(stats['total_star_count'], 2)
        self.assertEqual(stats['observed_last_month_count'], 2)
        self.assertEqual(stats['observed_by_you_count'], 0)

    def test_total_stats_with_observer(self):
        stats = Star.objects.get_total_stats(self.observer)
        self.assertEqual(stats['observed_by_you_count'], 2)


class StarModelTestCase(BaseTestCase):
    """
    Tests for Star model.
    """
    def setUp(self):
        super(StarModelTestCase, self).setUp()
        self._create_stars()

    def test_str(self):
        """
        String representation of a star is just its name.
        """
        self.assertEqual(str(self.star), self.star.name)

    def test_is_not_periodic(self):
        """
        Star without period or epoch is not periodic.
        """
        self.assertIsNone(self.star.period)
        self.assertIsNone(self.star.epoch)
        self.assertFalse(self.star.is_periodic())

    def test_is_not_periodic_only_period(self):
        """
        Period alone is not enough to consider the star periodic.
        """
        self.star.period = 309.95
        self.assertIsNone(self.star.epoch)
        self.assertFalse(self.star.is_periodic())

    def test_is_periodic(self):
        """
        Star is periodic only when it has a defined period and epoch.
        """
        self.assertIsNotNone(self.periodic_star.period)
        self.assertIsNotNone(self.periodic_star.epoch)
        self.assertTrue(self.periodic_star.is_periodic())

    def test_gcvs_name(self):
        """
        Check that space is replaced by + in GCVS search name.
        """
        self.assertEqual(self.star.get_gcvs_search_name(), 'R+LEO')

    def test_top_observers(self):
        """
        Check the list of people with most observations of the given star.
        """
        self._create_observations()
        expected = [
            {
                'observer_id': self.observer.id,
                'observer__aavso_code': self.observer.aavso_code,
                'observations_count': 5,
            },
            {
                'observer_id': self.observer2.id,
                'observer__aavso_code': self.observer2.aavso_code,
                'observations_count': 3,
            },
        ]
        top_observers = list(self.periodic_star.top_observers())
        self.assertEqual(top_observers, expected)

    def test_observers_count(self):
        self._create_observations()
        self.assertEqual(self.star.observers_count(), 1)
        self.assertEqual(self.periodic_star.observers_count(), 2)

    def test_recent_observations(self):
        self._create_observations()
        observations = self.periodic_star.recent_observations()
        self.assertEqual(observations[0].observer, self.observer2)

    def test_observations_by_observer(self):
        self._create_observations()
        observations = self.periodic_star.get_observations_by_observer(self.observer)
        self.assertEqual(observations.count(), 5)
        observations = self.periodic_star.get_observations_by_observer(self.observer2)
        self.assertEqual(observations.count(), 3)


class VariabilityTypeModelTestCase(BaseTestCase):
    """
    Tests for VariabilityType model.
    """
    def test_str(self):
        """
        String representation of variability type is its short GCVS code.
        """
        self._create_stars()
        self.assertEqual(str(self.variability_type), self.variability_type.code)
