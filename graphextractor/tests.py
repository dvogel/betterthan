"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from graphextractor.tweetparser import TweetLexer, TweetParser

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

class GraphExtractorTests(TestCase):
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
