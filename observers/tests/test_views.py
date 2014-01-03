# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.translation import ugettext_lazy as _

from djet.assertions import StatusCodeAssertionsMixin, MessagesAssertionsMixin
from djet.testcases import ViewTestCase
from djet.utils import refresh
from registration.backends.simple.views import RegistrationView

from ..models import Observer
from .. import views
from variablestars.tests.base import TestDataMixin


class RegisterTestCase(StatusCodeAssertionsMixin, MessagesAssertionsMixin, ViewTestCase):
    view_class = RegistrationView
    middleware_classes = [
        SessionMiddleware,
        MessageMiddleware,
    ]

    def test_invalid_form(self):
        request = self.factory.post(data={
            'username': 'newuser',
            'email': '',
        })
        response = self.view(request)
        self.assertContains(response, _('This field is required.'))

    def test_valid_form(self):
        request = self.factory.post(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'hunter2',
            'password2': 'hunter2',
        })
        response = self.view(request)
        observer = Observer.objects.get(user__username='newuser')
        self.assert_redirect(response, observer.get_absolute_url())
        self.assert_message_exists(request, messages.SUCCESS, _('Thank you for your registration!'))


class ObserverListViewTestCase(TestDataMixin, ViewTestCase):
    view_class = views.ObserverListView

    def test_response(self):
        self._create_users()
        request = self.factory.get()
        response = self.view(request)
        self.assertContains(response, self.observer.aavso_code)
        self.assertTemplateUsed(response, 'observers/observer_list.html')


class ObserverEditViewTestCase(StatusCodeAssertionsMixin, TestDataMixin, ViewTestCase):
    view_class = views.ObserverEditView

    def setUp(self):
        super(ObserverEditViewTestCase, self).setUp()
        self._create_users()

    def test_anonymous_user(self):
        request = self.factory.get(user=AnonymousUser())
        response = self.view(request)
        self.assert_redirect(response)

    def test_response(self):
        request = self.factory.get(user=self.user)
        response = self.view(request)
        self.assertContains(response, _("Edit profile"))
        self.assertTemplateUsed(response, 'observers/observer_edit.html')

    def test_update_observer_data(self):
        self.assertNotEqual(self.observer.limiting_magnitude, 11)
        request = self.factory.post(data={
            'limiting_magnitude': 11,
        }, user=self.user)
        response = self.view(request)
        self.assert_redirect(response, self.observer.get_absolute_url())
        observer = refresh(self.observer)
        self.assertEqual(observer.limiting_magnitude, 11)

    def test_update_user_data(self):
        self.assertNotEqual(self.user.first_name, 'Aaron')
        request = self.factory.post(data={
            'first_name': 'Aaron',
        }, user=self.user)
        response = self.view(request)
        self.assert_redirect(response, self.observer.get_absolute_url())
        user = refresh(self.user)
        self.assertEqual(user.first_name, 'Aaron')
