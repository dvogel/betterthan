from __future__ import division, print_function

import os
import logging

from tweeteater.models import Tweet
from graphextractor.models import EdgeTweet
from graphextractor.extractor import extract_edge_from_tweet_text

from celery import task


Log = logging.getLogger(os.path.basename(__file__)
                        if __name__ == "__main__"
                        else __name__)


@task(name='extract-edge')
def edge_extraction_task(tweet_pk):
    tweet = Tweet.objects.get(pk=tweet_pk)
    try:
        edge = extract_edge_from_tweet_text(tweet.text)
        edge_tweet = EdgeTweet.create_for_edge_and_tweet(edge, tweet)
        edge.tweets.add(edge_tweet)
    except ValueError as err:
        Log.error(u"Caught ValueError ({err}) while extracting edge from: {txt}".format(err=str(err), txt=tweet.text))

def queue_edge_extraction(tweet):
    edge_extraction_task.delay(tweet.pk)

