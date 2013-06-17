# coding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime
from copy import deepcopy
from django.utils import simplejson as json
from django.test import TestCase
from graphextractor.tweetparser import TweetLexer, TweetParser
from graphextractor.extractor import extract_edge_from_tweet_text

Tweet_0 = "http://anywhere.com #betterthan http://nowhere.com"
Tweet_1 = "http://duckduckgo.com #isbetterthan http://google.com for #privacy"
Tweet_2 = "http://www.opensecrets.org/ #isbetterthan http://fec.gov/ for #campaignfinance, and #opendata"
Tweet_3 = "jibberish and gobbly gook http://a.cz #betterthan http://b.info"
Tweet_4 = "http://a.cz #betterthan http://b.info mumbo jumbo and tall talk"
Tweet_5 = "http://anywhere.com/with/a/path/?and=a&query=string #betterthan http://nowhere.com"

def ilen(itr):
    n = 0
    for _ in itr:
        n += 1
    return n

def token_names_from_string(s):
    tokens = list(TweetLexer.lex(s))
    token_names = [tok.name for tok in tokens]
    return token_names

class TweetParserTests(TestCase):
    def test_lexer_tokens_0(self):
        token_names = token_names_from_string(Tweet_0)
        self.assertEqual(token_names, [u'URL', u'BTHASH', u'URL'])

    def test_lexer_tokens_1(self):
        token_names = token_names_from_string(Tweet_1)
        self.assertEqual(token_names, [u'URL', u'IBTHASH', u'URL',
                                       u'FOR', u'HASHTAG'])

    def test_lexer_tokens_2(self):
        token_names = token_names_from_string(Tweet_2)
        self.assertEqual(token_names, [u'URL', u'IBTHASH', u'URL',
                                       u'FOR', u'HASHTAG', u'HASHTAG'])

    def test_lexer_tokens_3(self):
        token_names = token_names_from_string(Tweet_3)
        self.assertEqual(token_names, [u'WORD', u'WORD', u'WORD',
                                       u'URL', u'BTHASH', u'URL'])

    def test_lexer_tokens_4(self):
        token_names = token_names_from_string(Tweet_4)
        self.assertEqual(token_names, [u'URL', u'BTHASH', u'URL',
                                       u'WORD', u'WORD', u'WORD', u'WORD'])

    def test_lexer_tokens_5(self):
        token_names = token_names_from_string(Tweet_5)
        self.assertEqual(token_names, [u'URL', u'BTHASH', u'URL'])

    def test_parser_structure_0(self):
        tweet = TweetParser.parse(TweetLexer.lex(Tweet_0))
        self.assertEqual(tweet, {'better_url': 'http://anywhere.com',
                                 'worse_url': 'http://nowhere.com',
                                 'topics': []})

    def test_parser_structure_1(self):
        tweet = TweetParser.parse(TweetLexer.lex(Tweet_1))
        self.assertEqual(tweet, {'better_url': 'http://duckduckgo.com',
                                 'worse_url': 'http://google.com',
                                 'topics': ['privacy']})

    def test_parser_structure_2(self):
        tweet = TweetParser.parse(TweetLexer.lex(Tweet_2))
        self.assertEqual(tweet, {'better_url': 'http://www.opensecrets.org/',
                                 'worse_url': 'http://fec.gov/',
                                 'topics': ['campaignfinance', 'opendata']})

    def test_parser_structure_3(self):
        tweet = TweetParser.parse(TweetLexer.lex(Tweet_3))
        self.assertEqual(tweet, {'better_url': 'http://a.cz',
                                 'worse_url': 'http://b.info',
                                 'topics': []})

    def test_parser_structure_4(self):
        tweet = TweetParser.parse(TweetLexer.lex(Tweet_4))
        self.assertEqual(tweet, {'better_url': 'http://a.cz',
                                 'worse_url': 'http://b.info',
                                 'topics': []})

    def test_parser_structure_5(self):
        tweet = TweetParser.parse(TweetLexer.lex(Tweet_5))
        self.assertEqual(tweet, {'better_url': 'http://anywhere.com/with/a/path/?and=a&query=string',
                                 'worse_url': 'http://nowhere.com',
                                 'topics': []})

class ExtractionTests(TestCase):
    def setUp(self):
        self.tweet = {
            'id': -1,
            'created_at': datetime.datetime.now(),
            'user': {
                'name': 'BetterThan',
                'screen_name': 'betterthanbot',
                'created_at': datetime.datetime.now(),
                'verified': False
            },
            'truncated': False,
            'lang': 'en',
            'retweeted': False,
            'retweet_count': 0,
            'text': None # text will be updated during tests
        }

    def test_tweet_0(self):
        edge = extract_edge_from_tweet_text(Tweet_0)
        self.addCleanup(edge.delete)
        self.assertEqual(edge.tweets.count(), 0)
        self.assertTrue(edge.topics.count() == 0)

    def test_tweet_1(self):
        edge = extract_edge_from_tweet_text(Tweet_1)
        self.addCleanup(edge.delete)
        self.assertEqual(edge.tweets.count(), 0)
        topic_names = [t.name for t in edge.topics.all()]
        self.assertEqual([u'privacy'], topic_names)

    def test_tweet_2(self):
        edge = extract_edge_from_tweet_text(Tweet_2)
        self.addCleanup(edge.delete)
        self.assertEqual(edge.tweets.count(), 0)
        topic_names = [t.name for t in edge.topics.all()]
        topic_names.sort()
        self.assertEqual([u'campaignfinance', u'opendata'], topic_names)
        
    def test_tweet_3(self):
        edge = extract_edge_from_tweet_text(Tweet_3)
        self.addCleanup(edge.delete)
        self.assertEqual(edge.tweets.count(), 0)
        topic_names = [t.name for t in edge.topics.all()]
        topic_names.sort()
        self.assertTrue(edge.topics.count() == 0)

    def test_tweet_4(self):
        edge = extract_edge_from_tweet_text(Tweet_4)
        self.addCleanup(edge.delete)
        self.assertEqual(edge.tweets.count(), 0)
        topic_names = [t.name for t in edge.topics.all()]
        topic_names.sort()
        self.assertTrue(edge.topics.count() == 0)

    def test_tweet_5(self):
        edge = extract_edge_from_tweet_text(Tweet_5)
        self.addCleanup(edge.delete)
        self.assertEqual(edge.tweets.count(), 0)
        topic_names = [t.name for t in edge.topics.all()]
        topic_names.sort()
        self.assertEqual(edge.topics.count(), 0)

