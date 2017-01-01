from django.contrib import messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from djet.assertions import InstanceAssertionsMixin, MessagesAssertionsMixin, StatusCodeAssertionsMixin
from djet.files import create_inmemory_file
from djet.testcases import ViewTestCase
from dj_pagination.middleware import PaginationMiddleware

from ..models import Observation
from .. import views
from variablestars.tests.base import TestDataMixin


class ObservationListViewTestCase(StatusCodeAssertionsMixin, TestDataMixin, ViewTestCase):
    view_class = views.ObservationListView
    middleware_classes = [
        PaginationMiddleware,
    ]

    def setUp(self):
        super().setUp()
        self._create_users()
        self._create_stars()
        self._create_observations()

    def test_list_observations_all_observers(self):
        request = self.factory.get()
        response = self.view(request)
        self.assertContains(response, str(self.observer))
        self.assertContains(response, str(self.observer2))

    def test_list_observations_single_observer(self):
        request = self.factory.get()
        response = self.view(request, observer_id=self.observer2.id)
        self.assertNotContains(response, str(self.observer))
        self.assertContains(response, str(self.observer2))


class AddObservationViewTestCase(InstanceAssertionsMixin, MessagesAssertionsMixin, StatusCodeAssertionsMixin, TestDataMixin, ViewTestCase):
    """
    Tests for ``observations.views.AddObservationView`` class.
    """
    view_class = views.AddObservationView
    middleware_classes = [
        SessionMiddleware,
        MessageMiddleware,
    ]

    def setUp(self):
        super().setUp()
        self._create_users()

    def test_response(self):
        """
        Check basic properties of the view.
        """
        request = self.factory.get(user=self.user)
        with self.assertTemplateUsed("observations/add_observation.html"):
            response = self.view(request)
            self.assertContains(response, _("Add new observation"))

    def test_predefined_star(self):
        """
        Check that one can add an observation with a predefined choice of star.
        """
        self._create_stars()
        request = self.factory.get(user=self.user)
        response = self.view(request, star_id=self.star.pk)
        self.assertContains(response, self.star.name)

    def test_form_invalid(self):
        """
        Check that invalid observation form displays meaningful errors.
        """
        request = self.factory.post(data={
        }, user=self.user)
        response = self.view(request)
        self.assertContains(response, _('This field is required.'))

    def test_form_valid(self):
        """
        A valid form creates new observation and redirects back to the form.
        """
        self._create_stars()
        with self.assert_instance_created(Observation, star=self.star, jd=2456634.1154, magnitude=7.1):
            request = self.factory.post(data={
                'star': self.star.id,
                'jd': '2456634.1154',
                'magnitude': '7.1',
            }, user=self.user)
            request.observer = self.observer
            response = self.view(request)
            self.assert_redirect(response, reverse('observations:add_observation'))
            self.assert_message_exists(request, messages.SUCCESS, _("Observation added successfully!"))


class UploadObservationsViewTestCase(InstanceAssertionsMixin, MessagesAssertionsMixin, StatusCodeAssertionsMixin, TestDataMixin, ViewTestCase):
    """
    Tests for ``observations.views.UploadObservationsView`` class.
    """
    view_class = views.UploadObservationsView
    middleware_classes = [
        SessionMiddleware,
        MessageMiddleware,
    ]

    def setUp(self):
        super().setUp()
        self._create_users()
        self._create_stars()
        self.lines = [
            "#TYPE=VISUAL",
            "#OBSCODE=%s" % self.observer.aavso_code,
            "#SOFTWARE=variablestars.net",
            "#DELIM=,",
            "#DATE=JD",
            "#OBSTYPE=Visual",
            "%s,2450702.1234,<11.1,na,110,113,070613,test3" % self.star.name,
        ]

    def test_response(self):
        request = self.factory.get(user=self.user)
        with self.assertTemplateUsed("observations/upload_observations.html"):
            response = self.view(request)
            self.assertContains(response, _("Upload observations"))

    def test_no_file(self):
        """
        If no file is selected, the form displays an error.
        """
        request = self.factory.post(data={
            'aavso_file': '',
        }, user=self.user)
        response = self.view(request)
        self.assertContains(response, _("This field is required."))

    def test_correct_file(self):
        """
        If the file is valid, observations are created.
        """
        contents = "\n".join(self.lines)
        aavso_file = create_inmemory_file('data.txt', contents.encode('utf-8'))
        with self.assert_instance_created(Observation, star=self.star, notes='test3'):
            request = self.factory.post(data={
                'aavso_file': aavso_file,
            }, user=self.user)
            request.observer = self.observer
            response = self.view(request)
            self.assert_redirect(response)
            self.assert_message_exists(request, messages.SUCCESS, _("File uploaded successfully!"))

    def test_malformed_file(self):
        """
        Check that a bad magnitude value raises an exception.
        """
        observations_count_before = Observation.objects.count()
        self.lines[-1] = "%s,2450702.1234,ASDF,na,110,113,070613,test3" % self.star.name
        contents = "\n".join(self.lines)
        aavso_file = create_inmemory_file('data.txt', contents.encode('utf-8'))
        request = self.factory.post(data={
            'aavso_file': aavso_file,
        }, user=self.user)
        request.observer = self.observer
        response = self.view(request)
        self.assert_redirect(response)
        self.assert_message_exists(request, messages.SUCCESS, _("File uploaded successfully!"))
        observations_count_after = Observation.objects.count()
        self.assertEqual(observations_count_after, observations_count_before)
