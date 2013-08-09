import hashlib
import tweeteater.models

from django.db import models
from utils import md5_digest

class Topic(models.Model):
    name = models.CharField(max_length=140,
                            null=False,
                            blank=False,
                            db_index=True,
                            primary_key=True)

class Edge(models.Model):
    # The actual URLs, used for
    # graph analysis.
    worse_url = models.TextField(null=False,
                                 blank=False,
                                 db_index=True)
    better_url = models.TextField(null=False,
                                  blank=False,
                                  db_index=True)

    # MD5 hashes of the urls for
    # ambiguous lookup.
    worse_md5 = models.CharField(max_length=32,
                                 null=False,
                                 blank=True,
                                 db_index=True)
    better_md5 = models.CharField(max_length=32,
                                  null=False,
                                  blank=True,
                                  db_index=True)

    topics = models.ManyToManyField(Topic, related_name='edges')

    # Moderation fields
    disabled = models.BooleanField(default=False)
    moderation_notes = models.TextField(null=True, blank=True)

    @classmethod
    def for_urls(cls, better_url, worse_url):
        (edge, created) = cls.objects.get_or_create(worse_url=worse_url,
                                                    better_url=better_url)
        return edge

    def save(self, *args, **kwargs):
        if self.worse_md5 in (None, u''):
            self.worse_md5 = md5_digest(self.worse_url)

        if self.better_md5 in (None, u''):
            self.better_md5 = md5_digest(self.better_url)

        super(Edge, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('worse_url', 'better_url')

def model_vars(obj):
    return dict(((fld.name, getattr(obj, fld.name))
                 for fld in obj._meta.fields))

class EdgeTweet(tweeteater.models.Tweet):
    edge = models.ForeignKey(Edge, related_name='tweets')

    @classmethod
    def create_for_edge_and_tweet(cls, edge, tweet):
        tweet_vars = model_vars(tweet)
        edge_tweet = EdgeTweet.objects.create(tweet_ptr=tweet,
                                              edge=edge,
                                              **tweet_vars)
        return edge_tweet

