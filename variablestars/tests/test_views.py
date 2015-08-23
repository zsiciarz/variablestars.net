from djet.assertions import StatusCodeAssertionsMixin
from djet.testcases import ViewTestCase

from observations.models import Observation
from observers.models import Observer
from stars.models import Star

from .base import TestDataMixin
from .. import views


class MainViewTestCase(StatusCodeAssertionsMixin, TestDataMixin, ViewTestCase):
    view_function = views.index

    def test_stats_for_anonymous_users(self):
        """
        Check that some basic stats are displayed for anonymous users.
        """
        self._create_users()
        self._create_stars()
        self._create_observations()
        request = self.factory.get(user=self.anonymous_user)
        response = self.view(request)
        self.assertContains(response, '<h1>%d</h1' % Star.objects.count())
        self.assertContains(response, '<h1>%d</h1' % Observer.objects.count())
        self.assertContains(response, '<h1>%d</h1' % Observation.objects.count())
