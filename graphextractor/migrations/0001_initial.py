# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table(u'graphextractor_topic', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140, primary_key=True, db_index=True)),
        ))
        db.send_create_signal(u'graphextractor', ['Topic'])

        # Adding model 'Edge'
        db.create_table(u'graphextractor_edge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('worse_url', self.gf('django.db.models.fields.TextField')(db_index=True)),
            ('better_url', self.gf('django.db.models.fields.TextField')(db_index=True)),
            ('worse_md5', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=32, blank=True)),
            ('better_md5', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=32, blank=True)),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('moderation_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'graphextractor', ['Edge'])

        # Adding unique constraint on 'Edge', fields ['worse_url', 'better_url']
        db.create_unique(u'graphextractor_edge', ['worse_url', 'better_url'])

        # Adding M2M table for field topics on 'Edge'
        db.create_table(u'graphextractor_edge_topics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('edge', models.ForeignKey(orm[u'graphextractor.edge'], null=False)),
            ('topic', models.ForeignKey(orm[u'graphextractor.topic'], null=False))
        ))
        db.create_unique(u'graphextractor_edge_topics', ['edge_id', 'topic_id'])

        # Adding model 'EdgeTweet'
        db.create_table(u'graphextractor_edgetweet', (
            (u'tweet_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tweeteater.Tweet'], unique=True, primary_key=True)),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tweets', to=orm['graphextractor.Edge'])),
        ))
        db.send_create_signal(u'graphextractor', ['EdgeTweet'])


    def backwards(self, orm):
        # Removing unique constraint on 'Edge', fields ['worse_url', 'better_url']
        db.delete_unique(u'graphextractor_edge', ['worse_url', 'better_url'])

        # Deleting model 'Topic'
        db.delete_table(u'graphextractor_topic')

        # Deleting model 'Edge'
        db.delete_table(u'graphextractor_edge')

        # Removing M2M table for field topics on 'Edge'
        db.delete_table('graphextractor_edge_topics')

        # Deleting model 'EdgeTweet'
        db.delete_table(u'graphextractor_edgetweet')


    models = {
        u'graphextractor.edge': {
            'Meta': {'unique_together': "(('worse_url', 'better_url'),)", 'object_name': 'Edge'},
            'better_md5': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'blank': 'True'}),
            'better_url': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderation_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'edges'", 'symmetrical': 'False', 'to': u"orm['graphextractor.Topic']"}),
            'worse_md5': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'blank': 'True'}),
            'worse_url': ('django.db.models.fields.TextField', [], {'db_index': 'True'})
        },
        u'graphextractor.edgetweet': {
            'Meta': {'object_name': 'EdgeTweet', '_ormbases': [u'tweeteater.Tweet']},
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tweets'", 'to': u"orm['graphextractor.Edge']"}),
            u'tweet_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tweeteater.Tweet']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'graphextractor.topic': {
            'Meta': {'object_name': 'Topic'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tweeteater.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'in_reply_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweeteater.Tweet']", 'null': 'True', 'blank': 'True'}),
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

    complete_apps = ['graphextractor']