import unittest
from unittest.mock import MagicMock

from ..middleware import StarFilterMiddleware


class StarFilterMiddlewareTestCase(unittest.TestCase):
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
