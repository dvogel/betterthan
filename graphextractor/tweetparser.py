import re
import itertools
from collections import deque
from rply import ParserGenerator, LexerGenerator
from graphextractor.rfc3987 import UrlPattern
from graphextractor.flattened import flattened

__all__ = ['TweetLexer', 'TweetParser']

lex = LexerGenerator()
lex.ignore(ur'(?:[,;\s]+|\band\b|\bor\b)+')
lex.add(u'URL', UrlPattern)
lex.add(u'BTHASH', ur'#betterthan')
lex.add(u'IBTHASH', ur'#isbetterthan')
lex.add(u'HASHTAG', ur'#[a-zA-Z0-9_]+')
lex.add(u'MENTION', ur'@[a-zA-Z0-9_]+')
lex.add(u'FOR', ur'(for|FOR|For)')
lex.add(u'WORD', ur'[\w]+')

pg = ParserGenerator([u'URL',
                      u'BTHASH',
                      u'IBTHASH',
                      u'HASHTAG',
                      u'MENTION',
                      u'FOR',
                      u'WORD'
                     ], 
                     cache_id=u'graphextractor.tweetparser')

@pg.production("betterthan : words URL bthash URL topics words")
def betterthan(p):
    ast = dict()
    ast.update(p[4])
    ast.update(better_url=p[1].value)
    ast.update(worse_url=p[3].value)
    return ast

@pg.production("bthash : BTHASH")
@pg.production("bthash : IBTHASH")
def bthash(p):
    return None

@pg.production("words : words WORD")
@pg.production("words : WORD")
@pg.production("words : ")
def words(p):
    return p

@pg.production("hashtags : hashtags HASHTAG")
@pg.production("hashtags : HASHTAG")
def hashtags(p):
    if len(p) == 1:
        return p
    else:
        return list(flattened(p))

@pg.production("topics : FOR hashtags")
@pg.production("topics : ")
def topics(p):
    if len(p) == 0:
        return { 'topics': [] }
    else:
        topics = [tok.value.strip('#') for tok in p[1]]
        return { 'topics': topics }

@pg.error
def error_handler(token):
    pos = token.getsourcepos().idx
    raise ValueError("Ran into a %s where it wasn't expected at offset %d" % (token.gettokentype(), pos))

TweetLexer = lex.build()
TweetParser = pg.build()

