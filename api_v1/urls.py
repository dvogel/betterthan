# coding: utf-8

from django.conf.urls import patterns, include, url
from api_v1.views import lookup_by_md5_prefix, graph_from_md5

urlpatterns = patterns('',
    url(r'^lookup/(?P<md5_prefix>[a-zA-Z0-9]{3,32})/$', lookup_by_md5_prefix,
        name=u'lookup-by-md5-prefix'),
    url(r'^graph/from/(?P<md5>[a-zA_Z0-9]{32})/$', graph_from_md5,
        name=u'graph-from-md5'),
)
