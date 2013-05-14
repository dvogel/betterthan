from __future__ import division, print_function

import tweepy

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tweeteater.basic import eat_tweets


class Command(BaseCommand):
    args = 'hashtag[, hashtah[, hashtag]]'
    help = 'Long-running task to ingest tweets for later processing.'

    def handle(self, *args, **options):

        if len(args) == 0:
            raise CommandError("You must specify a hashtag.")
        print(repr(args))
        hashtags = ['#' + hashtag.lstrip('#')
                    for hashtag in args]

        print("Ingesting tweets with hashtag(s): {}".format(", ".join(hashtags)))

        twitter_config = settings.TWITTER
        consumer_key = twitter_config['consumer_key']
        consumer_secret = twitter_config['consumer_secret']
        access_token = twitter_config['access_token']
        access_token_secret = twitter_config['access_token_secret']

        twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        twitter_auth.set_access_token(access_token, access_token_secret)
        
        try:
            username = twitter_auth.get_username()
            print("Authenticated as {user}".format(user=username))
        except tweepy.error.TweepError as e:
            raise CommandError(unicode(e))

        eat_tweets(twitter_auth, hashtags)

