from __future__ import division, print_function

import logging

import tweepy

from tweeteater.models import TwitterUser, Tweet, VerbatimTweet
from utils import dict_mget
from django.conf import settings


Log = logging.getLogger(os.path.basename(__file__)
                        if __name__ == "__main__"
                        else __name__)


class TweetListener(tweepy.streaming.StreamListener):
    def __init__(self, *args, **kwargs):
        super(TweetListener, self).__init__(self, *args, **kwargs)

    def on_data(self, data):
        tweet = Tweet.from_json(data)
        Log.info(u"Saved tweet #{0} from {1}".format(tweet.id,
                                                     tweet.user.screen_name))

    def on_timeout(self):
        Log.error(u"TweetListener connection timed out.")

    def on_error(self, status_code):
        Log.error(u"TweetListener got bad status code: {0}".format(status_code))


def eat_tweets(auth, hashtags):
    listener = TweetListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=hashtags)

