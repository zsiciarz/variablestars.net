# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser

from djet.assertions import StatusCodeAssertionsMixin
from djet.testcases import RequestFactory

from observations.models import Observation
from observers.models import Observer
from stars.models import Star

from .base import BaseTestCase
from .. import views


class MainViewTestCase(StatusCodeAssertionsMixin, BaseTestCase):
    def setUp(self):
        super(MainViewTestCase, self).setUp()
        self.anonymous_user = AnonymousUser()
        self.factory = RequestFactory()
        self.view = views.index

    def test_redirect_to_user_profile(self):
        request = self.factory.get(user=self.user)
        response = self.view(request)
        self.assert_redirect(response, self.user.get_absolute_url())

    def test_stats_for_anonymous_users(self):
        """
        Check that some basic stats are displayed for anonymous users.
        """
        request = self.factory.get(user=self.anonymous_user)
        response = self.view(request)
        self.assertContains(response, '<h1>%d</h1' % Star.objects.count())
        self.assertContains(response, '<h1>%d</h1' % Observer.objects.count())
        self.assertContains(response, '<h1>%d</h1' % Observation.objects.count())
