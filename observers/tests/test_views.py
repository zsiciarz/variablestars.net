from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _

from djet.assertions import StatusCodeAssertionsMixin
from djet.testcases import ViewTestCase
from dj_pagination.middleware import PaginationMiddleware

from .. import views
from variablestars.tests.base import TestDataMixin


class ObserverListViewTestCase(TestDataMixin, ViewTestCase):
    view_class = views.ObserverListView
    middleware_classes = [PaginationMiddleware]

    def test_response(self):
        self._create_users()
        request = self.factory.get()
        with self.assertTemplateUsed("observers/observer_list.html"):
            response = self.view(request)
            self.assertContains(response, self.observer.aavso_code)


class ObserverEditViewTestCase(StatusCodeAssertionsMixin, TestDataMixin, ViewTestCase):
    view_class = views.ObserverEditView

    def setUp(self):
        super().setUp()
        self._create_users()

    def test_anonymous_user(self):
        request = self.factory.get(user=AnonymousUser())
        response = self.view(request)
        self.assert_redirect(response)

    def test_response(self):
        request = self.factory.get(user=self.user)
        with self.assertTemplateUsed("observers/observer_edit.html"):
            response = self.view(request)
            self.assertContains(response, _("Edit profile"))

    def test_update_observer_data(self):
        self.assertNotEqual(self.observer.limiting_magnitude, 11)
        request = self.factory.post(data={"limiting_magnitude": 11}, user=self.user)
        response = self.view(request)
        self.assert_redirect(response, self.observer.get_absolute_url())
        self.observer.refresh_from_db()
        self.assertEqual(self.observer.limiting_magnitude, 11)

    def test_update_user_data(self):
        self.assertNotEqual(self.user.first_name, "Aaron")
        request = self.factory.post(data={"first_name": "Aaron"}, user=self.user)
        response = self.view(request)
        self.assert_redirect(response, self.observer.get_absolute_url())
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Aaron")
