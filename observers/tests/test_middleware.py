# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from django.contrib.auth.models import AnonymousUser, User

from mock import MagicMock, patch

from ..middleware import ObserverMiddleware
from ..models import Observer


class ObserverMiddlewareTestCase(unittest.TestCase):
    """
    Tests for ``observers.middleware.ObserverMiddleware`` class.
    """
    def setUp(self):
        super(ObserverMiddlewareTestCase, self).setUp()
        self.request = MagicMock()
        self.user = self.request.user = User(
            username='stargazer',
            email='stargazer@example.com',
            password='123456',
        )

    def test_authenticated_user(self):
        """
        Check that the middleware attaches an Observer instance to the request
        for authenticated users.
        """
        observer = Observer(user=self.user, aavso_code='XYZ')
        middleware = ObserverMiddleware()
        with patch.object(Observer.objects, 'get') as mock_get:
            mock_get.return_value = observer
            middleware.process_request(self.request)
            mock_get.assert_called_once_with(user=self.user)
        self.assertEqual(self.request.observer, observer)

    def test_anonymous_user(self):
        """
        Check that request.observer is None for anonymous users.
        """
        self.request.user = AnonymousUser()
        middleware = ObserverMiddleware()
        middleware.process_request(self.request)
        self.assertIsNone(self.request.observer)