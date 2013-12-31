# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from mock import MagicMock, patch

from ..middleware import ObserverMiddleware
from ..models import Observer
from variablestars.tests.base import BaseTestCase


class ObserverMiddlewareTestCase(BaseTestCase):
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


class LoginTestCase(BaseTestCase):
    def test_redirect_to_profile(self):
        url = reverse('auth_login')
        response = self.client.post(url, {
            'username': self.user.username,
            'password': '123456',
        }, follow=True)
        self.assertRedirects(response, self.observer.get_absolute_url())


class RegisterTestCase(BaseTestCase):
    def setUp(self):
        super(RegisterTestCase, self).setUp()
        self.url = reverse('registration_register')

    def test_invalid_form(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': '',
        })
        self.assertFormError(response, 'form', 'email', _('This field is required.'))

    def test_valid_form(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'hunter2',
            'password2': 'hunter2',
        }, follow=True)
        observer = Observer.objects.get(user__username='newuser')
        self.assertRedirects(response, observer.get_absolute_url())
        self.assertContains(response, _('Thank you for your registration!'))
        self.assertContains(response, _('Sign out'))


class ObserverListViewTestCase(BaseTestCase):
    def test_response(self):
        url = reverse('observers:observer_list')
        response = self.client.get(url)
        self.assertContains(response, self.observer.aavso_code)
        self.assertTemplateUsed(response, 'observers/observer_list.html')


class ObserverEditViewTestCase(BaseTestCase):
    def setUp(self):
        super(ObserverEditViewTestCase, self).setUp()
        self.url = reverse('observers:observer_edit')

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_login') + '?next=' + self.url)

    def test_response(self):
        self.client.login_observer()
        response = self.client.get(self.url)
        self.assertContains(response, _("Edit profile"))
        self.assertTemplateUsed(response, 'observers/observer_edit.html')

    def test_update_observer_data(self):
        self.client.login_observer()
        self.assertNotEqual(self.observer.limiting_magnitude, 11)
        response = self.client.post(self.url, {
            'limiting_magnitude': 11,
        })
        self.assertRedirects(response, self.observer.get_absolute_url())
        observer = Observer.objects.get(pk=self.observer.pk)
        self.assertEqual(observer.limiting_magnitude, 11)

    def test_update_user_data(self):
        self.client.login_observer()
        self.assertNotEqual(self.user.first_name, 'Aaron')
        self.client.post(self.url, {
            'first_name': 'Aaron',
        })
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.first_name, 'Aaron')
