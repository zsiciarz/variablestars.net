# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.core.urlresolvers import reverse

from mock import MagicMock

from ..admin import StarAdmin
from ..middleware import StarFilterMiddleware
from ..models import Star
from variablestars.tests.base import BaseTestCase


class StarAdminTestCase(BaseTestCase):
    """
    Tests for Star-related admin customizations.
    """
    def setUp(self):
        super(StarAdminTestCase, self).setUp()
        self.site = AdminSite()

    def test_queries_count(self):
        """
        Check that no extra queries are executed when iterating over queryset.
        """
        self._create_stars()
        admin = StarAdmin(Star, self.site)
        with self.assertNumQueries(1):
            stars = admin.get_queryset(request=None)
            types = [str(star.variability_type) for star in stars]
            self.assertEqual(len(types), 2)


class StarFilterMiddlewareTestCase(BaseTestCase):
    """
    Tests for ``stars.middleware.StarFilterMiddleware`` class.
    """
    def setUp(self):
        super(StarFilterMiddlewareTestCase, self).setUp()
        self.request = MagicMock()
        self.request.GET = {}
        self.request.session = {}

    def test_limiting_magnitude(self):
        """
        Check that the middleware stores limiting magnitude in current session.
        """
        middleware = StarFilterMiddleware()
        self.request.GET['limiting_magnitude'] = 9.0
        middleware.process_request(self.request)
        self.assertIn('limiting_magnitude', self.request.session)
        self.assertEqual(self.request.session['limiting_magnitude'], 9.0)

    def test_limiting_magnitude_none(self):
        """
        Check that 'None' value for limiting magnitude is a Pythonic None.
        """
        middleware = StarFilterMiddleware()
        self.request.GET['limiting_magnitude'] = 'None'
        middleware.process_request(self.request)
        self.assertIn('limiting_magnitude', self.request.session)
        self.assertIsNone(self.request.session['limiting_magnitude'])

    def test_stars_with_observations_true(self):
        """
        Check that 'True' value sets session attribute to True.
        """
        middleware = StarFilterMiddleware()
        self.request.GET['stars_with_observations'] = 'True'
        middleware.process_request(self.request)
        self.assertIn('stars_with_observations', self.request.session)
        self.assertTrue(self.request.session['stars_with_observations'])

    def test_stars_with_observations_false(self):
        """
        Check that other values set session attribute to False.
        """
        middleware = StarFilterMiddleware()
        self.request.GET['stars_with_observations'] = 'False'
        middleware.process_request(self.request)
        self.assertIn('stars_with_observations', self.request.session)
        self.assertFalse(self.request.session['stars_with_observations'])


class StarListViewTestCase(BaseTestCase):
    """
    Tests for ``stars.views.StarListView`` class.
    """
    def setUp(self):
        super(StarListViewTestCase, self).setUp()
        self._create_stars()
        self.star_without_observations = Star.objects.create(
            constellation='LEP',
            name='R LEP',
            ra='04:59:36.4',
            dec='-14:48:23',
            variability_type=self.variability_type,
            max_magnitude=5.5,
            min_magnitude=11.7,
        )
        # log in as some user and send a dummy request so that
        # client.session is a real session
        self.client.login_observer()
        self.client.get('/')

    def test_response(self):
        url = reverse('stars:star_list')
        response = self.client.get(url)
        self.assertContains(response, self.star.name)
        self.assertContains(response, self.periodic_star.name)
        self.assertContains(response, self.star_without_observations.name)
        self.assertTemplateUsed(response, "stars/star_list.html")

    def test_only_with_observations(self):
        self._create_observations()
        url = reverse('stars:star_list')
        session = self.client.session
        session['stars_with_observations'] = True
        session.save()
        response = self.client.get(url)
        self.assertContains(response, self.star.name)
        self.assertContains(response, self.periodic_star.name)
        self.assertNotContains(response, self.star_without_observations.name)

    def test_limiting_magnitude(self):
        url = reverse('stars:star_list')
        session = self.client.session
        session['limiting_magnitude'] = 5.0
        session.save()
        response = self.client.get(url)
        self.assertContains(response, self.star.name)
        self.assertNotContains(response, self.periodic_star.name)
        self.assertNotContains(response, self.star_without_observations.name)


class ConstellationListViewTestCase(BaseTestCase):
    def test_response(self):
        self._create_stars()
        url = reverse('stars:constellation_list', kwargs={
            'constellation': self.star.constellation,
        })
        response = self.client.get(url)
        self.assertContains(response, self.star.get_constellation_display())
        self.assertTemplateUsed(response, "stars/star_list.html")

    def test_filtered_stars(self):
        self._create_stars()
        url = reverse('stars:constellation_list', kwargs={'constellation': 'LEO'})
        response = self.client.get(url)
        self.assertContains(response, self.star.name)
        self.assertNotContains(response, self.periodic_star.name)


class StarSearchViewTestCase(BaseTestCase):
    def test_normal_search(self):
        self._create_stars()
        response = self.client.search_for_star(self.star.name[:4])
        self.assertContains(response, self.star.name)
        self.assertTemplateUsed(response, "stars/star_search.html")

    def test_exact_search(self):
        self._create_stars()
        response = self.client.search_for_star(self.star.name)
        self.assertRedirects(response, self.star.get_absolute_url())


class StarDetailViewTestCase(BaseTestCase):
    def test_response(self):
        self._create_stars()
        url = self.star.get_absolute_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "stars/star_detail.html")
        self.assertIsNotNone(response.context['next_rising'])

    def test_circumpolar_star(self):
        self._create_stars()
        self.star.dec = '+89:00:00'
        self.star.save()
        url = self.star.get_absolute_url()
        response = self.client.get(url)
        self.assertIsNone(response.context['next_rising'])


class VariabilityTypeDetailViewTestCase(BaseTestCase):
    def test_response(self):
        self._create_stars()
        url = self.variability_type.get_absolute_url()
        response = self.client.get(url)
        self.assertTemplateUsed("stars/variabilitytype_detail.html")
        self.assertContains(response, self.variability_type.long_description)


class RecentObservationsTestCase(BaseTestCase):
    def setUp(self):
        super(RecentObservationsTestCase, self).setUp()
        self._create_stars()
        self._create_observations()
        self.url = reverse('stars:recent_observations', kwargs={'pk': self.star.pk})

    def test_csv_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response['Content-Type'], 'text/csv')
