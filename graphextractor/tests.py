"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from graphextractor.tweetparser import TweetLexer

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

class GraphExtractorTests(TestCase):
    def test_lexer_word_count_1(self):
        """
        Tests the whitespace splitting.
        """
        words = TweetLexer(Tweet_1)
        cnt = ilen(words)
        self.assertEqual(cnt, 5)

    def test_lexer_word_count_2(self):
        """
        Tests the whitespace splitting.
        """
        words = TweetLexer(Tweet_2)
        cnt = ilen(words)
        self.assertEqual(cnt, 6)


