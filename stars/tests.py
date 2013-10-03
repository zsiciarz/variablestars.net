# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from variablestars.tests import BaseTestCase


class StarModelTestCase(BaseTestCase):
    """
    Tests for Star model.
    """

    def test_str(self):
        """
        String representation of a star is just its name.
        """
        self.assertEqual(str(self.star), self.star.name)

    def test_is_not_periodic(self):
        """
        Star without period or epoch is not periodic.
        """
        self.assertIsNone(self.star.period)
        self.assertIsNone(self.star.epoch)
        self.assertFalse(self.star.is_periodic())

    def test_is_not_periodic_only_period(self):
        """
        Period alone is not enough to consider the star periodic.
        """
        self.star.period = 309.95
        self.assertIsNone(self.star.epoch)
        self.assertFalse(self.star.is_periodic())

    def test_is_periodic(self):
        """
        Star is periodic only when it has a defined period and epoch.
        """
        self.assertIsNotNone(self.periodic_star.period)
        self.assertIsNotNone(self.periodic_star.epoch)
        self.assertTrue(self.periodic_star.is_periodic())
