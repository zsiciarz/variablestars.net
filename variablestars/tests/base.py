from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from djet.testcases import RequestFactory

from observations.models import Observation
from observations.utils import jd_now
from stars.models import Star, VariabilityType


class ObserverClient(Client):
    """
    An extended test client customized for this site.

    Inspired by:
    http://slid.es/wojtekerbetowski-1/advanced-testing-django-applications
    """
    def __init__(self, user, password):
        """
        We need to pass password explicitly here.
        """
        self.user = user
        self.observer = user.observer
        self.password = password
        super().__init__()

    def login_observer(self):
        return self.login(username=self.user.username, password=self.password)

    def search_for_star(self, star_name):
        url = reverse('stars:star_search')
        return self.get(url, {'q': star_name})


class TestDataMixin(object):
    @classmethod
    def _create_users(cls):
        cls.user = User.objects.create_user(
            'stargazer',
            'stargazer@example.com',
            '123456',
        )
        cls.anonymous_user = AnonymousUser()
        cls.observer = cls.user.observer
        cls.observer.aavso_code = 'XYZ'
        cls.observer.save()
        cls.user2 = User.objects.create_user(
            'kepler',
            'kepler@example.com',
            'johannes',
        )
        cls.observer2 = cls.user2.observer
        cls.observer2.aavso_code = 'JKL'
        cls.observer2.save()

    @classmethod
    def _create_stars(cls):
        cls.variability_type = VariabilityType.objects.create(
            code='M',
            long_description='Mira stars',
        )
        cls.star = Star.objects.create(
            constellation='LEO',
            name='R LEO',
            ra='09:47:33.5',
            dec='+11:25:44',
            variability_type=cls.variability_type,
            max_magnitude=4.4,
            min_magnitude=11.3,
            period=None,
            epoch=None,
        )
        cls.periodic_star = Star.objects.create(
            constellation='CEP',
            name='T CEP',
            ra='21:09:31.8',
            dec='+68:29:27',
            variability_type=cls.variability_type,
            max_magnitude=5.2,
            min_magnitude=11.3,
            period=388.14,
            epoch=2444177.0,
        )

    @classmethod
    def _create_observations(cls):
        observations = []
        for i in range(10):
            observations.append(Observation(
                observer=cls.observer,
                star=cls.star,
                jd=jd_now() - i,
                magnitude=8.5 + 0.1 * i,
            ))
        for i in range(5):
            observations.append(Observation(
                observer=cls.observer,
                star=cls.periodic_star,
                jd=jd_now() - 30 - i,
                magnitude=6.5 - 0.2 * i,
            ))
        for i in range(3):
            observations.append(Observation(
                observer=cls.observer2,
                star=cls.periodic_star,
                jd=jd_now() - 10 - 0.05 * i,
                magnitude=6.4 - 0.25 * i,
            ))
        Observation.objects.bulk_create(observations)
        # bulk_create doesn't call save(), so we update denormalized fields
        cls.star.observations_count = 10
        cls.star.save()
        cls.periodic_star.observations_count = 8
        cls.periodic_star.save()


class BaseTestCase(TestDataMixin, TestCase):
    """
    Base test class for other test cases to derive from.
    """
    @classmethod
    def setUpTestData(cls):
        cls._create_users()

    def setUp(self):
        self.factory = RequestFactory()
        self.client = ObserverClient(self.user, '123456')
