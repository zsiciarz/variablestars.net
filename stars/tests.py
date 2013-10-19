# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from mock import MagicMock

from .middleware import StarFilterMiddleware
from .models import Star
from variablestars.tests import BaseTestCase


class StarQuerySetTestCase(BaseTestCase):
    """
    Tests for ``StarQuerySet`` class.
    """

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


class VariabilityTypeModelTestCase(BaseTestCase):
    """
    Tests for VariabilityType model.
    """
    def test_str(self):
        """
        String representation of variability type is its short GCVS code.
        """
        self.assertEqual(str(self.variability_type), self.variability_type.code)


class StarFilterMiddlewareTestCase(BaseTestCase):
    """
    Tests for ``stars.middleware.StarFilterMiddleware`` class.
    """
    def setUp(self):
        super(StarFilterMiddlewareTestCase, self).setUp()
        self.request = MagicMock()
        self.request.GET = {}
        self.request.session = {}

    def test_limiting_magnitude(self):
        """
        Check that the middleware stores limiting magnitude in current session.
        """
        middleware = StarFilterMiddleware()
        self.request.GET['limiting_magnitude'] = 9.0
        middleware.process_request(self.request)
        self.assertIn('limiting_magnitude', self.request.session)
        self.assertEqual(self.request.session['limiting_magnitude'], 9.0)

    def test_limiting_magnitude_none(self):
        """
        Check that 'None' value for limiting magnitude is a Pythonic None.
        """
        middleware = StarFilterMiddleware()
        self.request.GET['limiting_magnitude'] = 'None'
        middleware.process_request(self.request)
        self.assertIn('limiting_magnitude', self.request.session)
        self.assertIsNone(self.request.session['limiting_magnitude'])

    def test_stars_with_observations_true(self):
        """
        Check that 'True' value sets session attribute to True.
        """
        middleware = StarFilterMiddleware()
        self.request.GET['stars_with_observations'] = 'True'
        middleware.process_request(self.request)
        self.assertIn('stars_with_observations', self.request.session)
        self.assertTrue(self.request.session['stars_with_observations'])

    def test_stars_with_observations_false(self):
        """
        Check that other values set session attribute to False.
        """
        middleware = StarFilterMiddleware()
        self.request.GET['stars_with_observations'] = 'False'
        middleware.process_request(self.request)
        self.assertIn('stars_with_observations', self.request.session)
        self.assertFalse(self.request.session['stars_with_observations'])


class StarListViewTestCase(BaseTestCase):
    """
    Tests for ``stars.views.StarListView`` class.
    """
    def setUp(self):
        super(StarListViewTestCase, self).setUp()
        self.star_without_observations = Star.objects.create(
            constellation='LEP',
            name='R LEP',
            ra='04:59:36.4',
            dec='-14:48:23',
            variability_type=self.variability_type,
            max_magnitude=5.5,
            min_magnitude=11.7,
        )
        # log in as some user and send a dummy request so that
        # client.session is a real session
        self.client.login(username='stargazer', password='123456')
        self.client.get('/')

    def test_response(self):
        url = reverse('stars:star_list')
        response = self.client.get(url)
        self.assertContains(response, self.star.name)
        self.assertContains(response, self.periodic_star.name)
        self.assertContains(response, self.star_without_observations.name)
        self.assertTemplateUsed(response, "stars/star_list.html")

    def test_only_with_observations(self):
        url = reverse('stars:star_list')
        session = self.client.session
        session['stars_with_observations'] = True
        session.save()
        response = self.client.get(url)
        self.assertContains(response, self.star.name)
        self.assertContains(response, self.periodic_star.name)
        self.assertNotContains(response, self.star_without_observations.name)

    def test_limiting_magnitude(self):
        url = reverse('stars:star_list')
        session = self.client.session
        session['limiting_magnitude'] = 5.0
        session.save()
        response = self.client.get(url)
        self.assertContains(response, self.star.name)
        self.assertNotContains(response, self.periodic_star.name)
        self.assertNotContains(response, self.star_without_observations.name)
