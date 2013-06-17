"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from utils import dict_mget


class SimpleTest(TestCase):
    def setUp(self):
        self.person = {
            'name': {
                'first': 'Drew',
                'last': 'Vogel'
            },
            'gender': 'male'
        }

    def test_mget_simple(self):
        first_name = dict_mget(self.person,
                               ['name', 'first'])
        self.assertEqual(first_name, 'Drew')

    def test_mget_default(self):
        middle_name = dict_mget(self.person,
                                ['name', 'middle'],
                                'Preston')
        self.assertEqual(middle_name, 'Preston')

    def test_mget_shallow(self):
        gender = dict_mget(self.person, ['gender'], 'female')
        self.assertEqual(gender, 'male')

    def test_mget_missing(self):
        dob = dict_mget(self.person, ['dob'])
        self.assertEqual(dob, None)

