# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from mock import MagicMock

from .middleware import ObserverMiddleware
from .models import Observer
from observations.models import Observation
from variablestars.tests import BaseTestCase


class ObserverModelTestCase(BaseTestCase):
    """
    Tests for Observer model.
    """

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

    def test_recent_observations(self):
        observations = self.observer.recent_observations()
        self.assertEqual(observations[0].star, self.star)
        observations = self.observer2.recent_observations()
        self.assertEqual(observations[0].star, self.periodic_star)

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


class ObserverQuerySetTestCase(ObserverModelTestCase):
    """
    Tests for ObserverQuerySet class (accessed through a manager).
    """

    def test_observations_count(self):
        """
        Check that returned Observer instances have are annotated with
        number of observations.
        """
        observers = Observer.objects.with_observations_count().order_by('pk')
        self.assertEqual(observers[0], self.observer)
        observations_count = Observation.objects.filter(
            observer=self.observer
        ).count()
        self.assertEqual(observers[0].observations_count, observations_count)

    def test_total_stats(self):
        stats = Observer.objects.get_total_stats()
        self.assertEqual(stats['total_observer_count'], 2)


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
