import unittest
from unittest.mock import MagicMock

from variablestars.tests.base import get_response
from ..middleware import star_filter_middleware


class StarFilterMiddlewareTestCase(unittest.TestCase):
    """
    Tests for ``stars.middleware.star_filter_middleware`` function.
    """

    def setUp(self):
        super().setUp()
        self.request = MagicMock()
        self.request.GET = {}
        self.request.session = {}

    def test_limiting_magnitude(self):
        """
        Check that the middleware stores limiting magnitude in current session.
        """
        middleware = star_filter_middleware(get_response)
        self.request.GET["limiting_magnitude"] = 9.0
        middleware(self.request)
        self.assertIn("limiting_magnitude", self.request.session)
        self.assertEqual(self.request.session["limiting_magnitude"], 9.0)

    def test_limiting_magnitude_none(self):
        """
        Check that 'None' value for limiting magnitude is a Pythonic None.
        """
        middleware = star_filter_middleware(get_response)
        self.request.GET["limiting_magnitude"] = "None"
        middleware(self.request)
        self.assertIn("limiting_magnitude", self.request.session)
        self.assertIsNone(self.request.session["limiting_magnitude"])

    def test_stars_with_observations_true(self):
        """
        Check that 'True' value sets session attribute to True.
        """
        middleware = star_filter_middleware(get_response)
        self.request.GET["stars_with_observations"] = "True"
        middleware(self.request)
        self.assertIn("stars_with_observations", self.request.session)
        self.assertTrue(self.request.session["stars_with_observations"])

    def test_stars_with_observations_false(self):
        """
        Check that other values set session attribute to False.
        """
        middleware = star_filter_middleware(get_response)
        self.request.GET["stars_with_observations"] = "False"
        middleware(self.request)
        self.assertIn("stars_with_observations", self.request.session)
        self.assertFalse(self.request.session["stars_with_observations"])
