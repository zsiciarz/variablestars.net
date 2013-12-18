# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from observations.models import Observation
from observers.models import Observer
from stars.models import Star

from .base import BaseTestCase


class MainViewTestCase(BaseTestCase):
    def setUp(self):
        super(MainViewTestCase, self).setUp()
        self.url = reverse('main')

    def test_redirect_to_user_profile(self):
        self.client.login_observer()
        response = self.client.get(self.url)
        self.assertRedirects(response, self.observer.get_absolute_url())

    def test_stats_for_anonymous_users(self):
        """
        Check that some basic stats are displayed for anonymous users.
        """
        response = self.client.get(self.url)
        self.assertContains(response, '<h1>%d</h1' % Star.objects.count())
        self.assertContains(response, '<h1>%d</h1' % Observer.objects.count())
        self.assertContains(response, '<h1>%d</h1' % Observation.objects.count())
