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
        self.assertFalse(self.star.is_periodic())
