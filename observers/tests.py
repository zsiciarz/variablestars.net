# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser

from mock import MagicMock

from .middleware import ObserverMiddleware
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


class ObserverMiddlewareTestCase(BaseTestCase):
    """
    Tests for ``observers.middleware.ObserverMiddleware`` class.
    """
    def setUp(self):
        super(ObserverMiddlewareTestCase, self).setUp()
        self.request = MagicMock()
        self.request.user = self.user

    def test_authenticated_user(self):
        """
        Check that the middleware attaches an Observer instance to the request
        for authenticated users.
        """
        middleware = ObserverMiddleware()
        middleware.process_request(self.request)
        self.assertEqual(self.request.observer, self.observer)

    def test_anonymous_user(self):
        """
        Check that request.observer is None for anonymous users.
        """
        self.request.user = AnonymousUser()
        middleware = ObserverMiddleware()
        middleware.process_request(self.request)
        self.assertIsNone(self.request.observer)
