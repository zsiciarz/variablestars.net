# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from mock import MagicMock

from .middleware import StarFilterMiddleware
from variablestars.tests import BaseTestCase


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
