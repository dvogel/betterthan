# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tweet.verbatim_tweet'
        db.alter_column(u'tweeteater_tweet', 'verbatim_tweet_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tweeteater.VerbatimTweet'], unique=True))
        # Adding unique constraint on 'Tweet', fields ['verbatim_tweet']
        db.create_unique(u'tweeteater_tweet', ['verbatim_tweet_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tweet', fields ['verbatim_tweet']
        db.delete_unique(u'tweeteater_tweet', ['verbatim_tweet_id'])


        # Changing field 'Tweet.verbatim_tweet'
        db.alter_column(u'tweeteater_tweet', 'verbatim_tweet_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweeteater.VerbatimTweet']))

    models = {
        u'tweeteater.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'retweet_count': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'retweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}),
            'truncated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweeteater.TwitterUser']"}),
            'verbatim_tweet': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tweeteater.VerbatimTweet']", 'unique': 'True'})
        },
        u'tweeteater.twitteruser': {
            'Meta': {'object_name': 'TwitterUser'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'tweeteater.verbatimtweet': {
            'Meta': {'object_name': 'VerbatimTweet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['tweeteater']