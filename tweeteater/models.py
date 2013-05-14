import json

from django.db import models
from dateutil.parser import parse as parse_datetime

class TwitterUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(db_index=True)
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.screen_name)
   
class VerbatimTweet(models.Model):
    id = models.AutoField(primary_key=True)
    json = models.TextField()


class Tweet(models.Model):
    # These fields come from the tweet object.
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(db_index=True)
    lang = models.CharField(max_length=4, null=True)
    retweeted = models.BooleanField(default=False)
    retweet_count = models.IntegerField(db_index=True)
    text = models.CharField(max_length=140, db_index=True)
    truncated = models.BooleanField()
    user = models.ForeignKey(TwitterUser)
    verbatim_tweet = models.ForeignKey(VerbatimTweet)

    # Status fields based on events occuring after the 
    # tweet is first logged.
    deleted = models.BooleanField(default=False)

    @staticmethod
    def from_json(json_str):
        verbatim_tweet = VerbatimTweet()
        verbatim_tweet.json = json_str
        verbatim_tweet.save()

        obj = json.loads(json_str)
        tweet = Tweet()
        tweet.verbatim_tweet = verbatim_tweet
        tweet.id = obj['id']
        tweet.created_at = parse_datetime(obj['created_at'])
        for field in ['lang', 'retweeted', 'retweet_count',
                      'text', 'truncated']:
            setattr(tweet, field, obj.get(field))

        user_obj = obj['user']
        user_created_at = parse_datetime(user_obj['created_at'])
        (user, created) = TwitterUser.objects.get_or_create(id=user_obj['id'],
                                                            defaults={'created_at': user_created_at})
        if created:
            user.name = user_obj.get('name')
            user.screen_name = user_obj.get('screen_name')
            user.verified = user_obj.get('verified')
            user.save()
        tweet.user = user

        tweet.save()
        return tweet



