# coding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import simplejson as json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from graphextractor.models import Edge

class KnownKnowns(TestCase):

    def setUp(self):
        self.known_edge = Edge.for_urls(worse_url=u'http://worse/is/worse',
                                        better_url=u'http://better/is/better')
        self.known_edge.save()
        self.addCleanup(self.known_edge.delete)

    def test_md5_generation(self):
        self.assertTrue(self.known_edge.worse_md5 is not None)
        self.assertTrue(self.known_edge.worse_md5 is not u'')
        self.assertTrue(self.known_edge.better_md5 is not None)
        self.assertTrue(self.known_edge.better_md5 is not u'')

    def test_found_worse(self):
        client = Client()
        resp = client.get(reverse(u'lookup-by-md5-prefix',
                                  args=[self.known_edge.worse_md5]))
        result = json.loads(resp.content)
        self.assertTrue(u'better' in result)
        self.assertTrue(len(result[u'better']) > 0)
        self.assertTrue(self.known_edge.better_url in result[u'better'])

    def test_found_worse_prefix(self):
        client = Client()
        resp = client.get(reverse(u'lookup-by-md5-prefix',
                                  args=[self.known_edge.worse_md5[:4]]))
        result = json.loads(resp.content)
        self.assertTrue(u'better' in result)
        self.assertTrue(len(result[u'better']) > 0)
        self.assertTrue(self.known_edge.better_url in result[u'better'])

    def test_found_better(self):
        client = Client()
        resp = client.get(reverse(u'lookup-by-md5-prefix',
                                  args=[self.known_edge.better_md5]))
        result = json.loads(resp.content)
        self.assertTrue(u'worse' in result)
        self.assertTrue(len(result[u'worse']) > 0)
        self.assertTrue(self.known_edge.worse_url in result[u'worse'])


    def test_found_better_prefix(self):
        client = Client()
        resp = client.get(reverse(u'lookup-by-md5-prefix',
                                  args=[self.known_edge.better_md5[:4]]))
        result = json.loads(resp.content)
        self.assertTrue(u'worse' in result)
        self.assertTrue(len(result[u'worse']) > 0)
        self.assertTrue(self.known_edge.worse_url in result[u'worse'])

