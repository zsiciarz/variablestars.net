import unittest

from ..models import Star, VariabilityType
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


class StarModelBasicPropertiesTestCase(unittest.TestCase):
    """
    Tests for Star model - basic properties.
    """
    def test_str(self):
        """
        String representation of a star is just its name.
        """
        star = Star(name='R LEO')
        self.assertEqual(str(star), star.name)

    def test_is_not_periodic(self):
        """
        Star without period or epoch is not periodic.
        """
        star = Star(name='R LEO', period=None, epoch=None)
        self.assertFalse(star.is_periodic())

    def test_is_not_periodic_only_period(self):
        """
        Period alone is not enough to consider the star periodic.
        """
        star = Star(name='R LEO', period=309.95, epoch=None)
        self.assertFalse(star.is_periodic())

    def test_is_periodic(self):
        """
        Star is periodic only when it has a defined period and epoch.
        """
        star = Star(name='T CEP', period=388.14, epoch=2444177.0)
        self.assertTrue(star.is_periodic())

    def test_gcvs_name(self):
        """
        Check that space is replaced by + in GCVS search name.
        """
        star = Star(name='R LEO')
        self.assertEqual(star.get_gcvs_search_name(), 'R+LEO')


class StarObservationsModelTestCase(BaseTestCase):
    """
    Tests for Star model - features related to observations.
    """
    def setUp(self):
        super(StarObservationsModelTestCase, self).setUp()
        self._create_stars()
        self._create_observations()

    def test_top_observers(self):
        """
        Check the list of people with most observations of the given star.
        """
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
        self.assertEqual(self.star.observers_count(), 1)
        self.assertEqual(self.periodic_star.observers_count(), 2)

    def test_recent_observations(self):
        observations = self.periodic_star.recent_observations()
        self.assertEqual(observations[0].observer, self.observer2)

    def test_observations_by_observer(self):
        observations = self.periodic_star.get_observations_by_observer(self.observer)
        self.assertEqual(observations.count(), 5)
        observations = self.periodic_star.get_observations_by_observer(self.observer2)
        self.assertEqual(observations.count(), 3)


class VariabilityTypeModelTestCase(unittest.TestCase):
    """
    Tests for VariabilityType model.
    """
    def test_str(self):
        """
        String representation of variability type is its short GCVS code.
        """
        variability_type = VariabilityType(
            code='M',
            long_description='Mira stars',
        )
        self.assertEqual(str(variability_type), variability_type.code)
