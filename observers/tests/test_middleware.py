from unittest.mock import MagicMock, patch

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase

from variablestars.tests.base import get_response
from ..middleware import observer_middleware
from ..models import Observer


class ObserverMiddlewareTestCase(TestCase):
    """
    Tests for ``observers.middleware.observer_middleware`` function.
    """
    def setUp(self):
        super().setUp()
        self.request = MagicMock()
        self.user = self.request.user = User.objects.create_user(
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
        middleware = observer_middleware(get_response)
        with patch.object(Observer.objects, 'get') as mock_get:
            mock_get.return_value = observer
            middleware(self.request)
            mock_get.assert_called_once_with(user=self.user)
        self.assertEqual(self.request.observer, observer)

    def test_anonymous_user(self):
        """
        Check that request.observer is None for anonymous users.
        """
        self.request.user = AnonymousUser()
        middleware = observer_middleware(get_response)
        middleware(self.request)
        self.assertIsNone(self.request.observer)
