# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwitterUser'
        db.create_table(u'tweeteater_twitteruser', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tweeteater', ['TwitterUser'])

        # Adding model 'VerbatimTweet'
        db.create_table(u'tweeteater_verbatimtweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('json', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'tweeteater', ['VerbatimTweet'])

        # Adding model 'Tweet'
        db.create_table(u'tweeteater_tweet', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('retweeted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('retweet_count', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140, db_index=True)),
            ('truncated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweeteater.TwitterUser'])),
            ('verbatim_tweet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweeteater.VerbatimTweet'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tweeteater', ['Tweet'])


    def backwards(self, orm):
        # Deleting model 'TwitterUser'
        db.delete_table(u'tweeteater_twitteruser')

        # Deleting model 'VerbatimTweet'
        db.delete_table(u'tweeteater_verbatimtweet')

        # Deleting model 'Tweet'
        db.delete_table(u'tweeteater_tweet')


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
            'verbatim_tweet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweeteater.VerbatimTweet']"})
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