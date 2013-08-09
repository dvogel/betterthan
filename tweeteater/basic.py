from __future__ import division, print_function

import os
import logging

import tweepy

from tweeteater.models import Tweet


Log = logging.getLogger(os.path.basename(__file__)
                        if __name__ == "__main__"
                        else __name__)


class TweetListener(tweepy.streaming.StreamListener):
    def __init__(self, on_tweet=None, *args, **kwargs):
        super(TweetListener, self).__init__(self, *args, **kwargs)
        self.on_tweet = on_tweet

    def on_data(self, data):
        tweet = Tweet.from_json(data)
        Log.info(u"Saved tweet #{0} from {1}".format(tweet.id,
                                                     tweet.user.screen_name))
        if callable(self.on_tweet):
            try:
                self.on_tweet(tweet)
            except Exception as e:
                Log.error("Exception caught in on_tweet task {on_tweet}: {e}".format(on_tweet=str(self.on_tweet), e=str(e)))

    def on_timeout(self):
        Log.error(u"TweetListener connection timed out.")

    def on_error(self, status_code):
        Log.error(u"TweetListener got bad status code: {0}".format(status_code))


def eat_tweets(auth, hashtags, on_tweet=None):
    listener = TweetListener(on_tweet=on_tweet)
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=hashtags)

