# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from djet.assertions import InstanceAssertionsMixin
from djet.files import create_inmemory_file

from ..models import Observation
from variablestars.tests.base import BaseTestCase


class AddObservationViewTestCase(InstanceAssertionsMixin, BaseTestCase):
    """
    Tests for ``observations.views.AddObservationView`` class.
    """
    def setUp(self):
        super(AddObservationViewTestCase, self).setUp()
        self.url = reverse('observations:add_observation')
        self.client.login_observer()

    def test_response(self):
        """
        Check basic properties of the view.
        """
        response = self.client.get(self.url)
        self.assertContains(response, _("Add new observation"))
        self.assertTemplateUsed(response, "observations/add_observation.html")

    def test_predefined_star(self):
        """
        Check that one can add an observation with a predefined choice of star.
        """
        url = reverse('observations:add_observation_for_star', args=[], kwargs={
            'star_id': self.star.pk,
        })
        response = self.client.get(url)
        self.assertContains(response, self.star.name)

    def test_form_invalid(self):
        """
        Check that invalid observation form displays meaningful errors.
        """
        response = self.client.post(self.url, {
        })
        self.assertFormError(response, 'form', 'star', _('This field is required.'))
        self.assertFormError(response, 'form', 'jd', _('This field is required.'))
        self.assertFormError(response, 'form', 'magnitude', _('This field is required.'))

    def test_form_valid(self):
        """
        A valid form creates new observation and redirects back to the form.
        """
        with self.assert_instance_created(Observation, star=self.star, jd=2456634.1154, magnitude=7.1):
            response = self.client.post(self.url, {
                'star': self.star.id,
                'jd': '2456634.1154',
                'magnitude': '7.1',
            }, follow=True)
            self.assertRedirects(response, self.url)
            self.assertContains(response, _("Observation added successfully!"))


class UploadObservationsViewTestCase(InstanceAssertionsMixin, BaseTestCase):
    """
    Tests for ``observations.views.UploadObservationsView`` class.
    """
    def setUp(self):
        super(UploadObservationsViewTestCase, self).setUp()
        self.url = reverse('observations:upload_observations')
        self.client.login_observer()
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
        response = self.client.get(self.url)
        self.assertContains(response, _("Upload observations"))
        self.assertTemplateUsed(response, "observations/upload_observations.html")

    def test_no_file(self):
        """
        If no file is selected, the form displays an error.
        """
        response = self.client.post(self.url, {
            'aavso_file': '',
        })
        self.assertFormError(response, 'form', 'aavso_file', _("This field is required."))

    def test_correct_file(self):
        """
        If the file is valid, observations are created.
        """
        aavso_file = create_inmemory_file('data.txt', "\n".join(self.lines))
        with self.assert_instance_created(Observation, star=self.star, notes='test3'):
            response = self.client.post(self.url, {
                'aavso_file': aavso_file,
            }, follow=True)
            self.assertContains(response, _("File uploaded successfully!"))

    def test_malformed_file(self):
        """
        Check that a bad magnitude value raises an exception.
        """
        observations_count_before = Observation.objects.count()
        self.lines[-1] = "%s,2450702.1234,ASDF,na,110,113,070613,test3" % self.star.name
        aavso_file = create_inmemory_file('data.txt', "\n".join(self.lines))
        response = self.client.post(self.url, {
            'aavso_file': aavso_file,
        }, follow=True)
        self.assertContains(response, _("File uploaded successfully!"))
        observations_count_after = Observation.objects.count()
        self.assertEqual(observations_count_after, observations_count_before)
