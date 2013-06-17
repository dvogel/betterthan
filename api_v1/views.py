# coding: utf-8

from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from graphextractor.models import EdgeTweet, Topic, Edge

TRUTH_STRINGS = ['y', 'yes', 'true', 't']

class JSONResponse(HttpResponse):
    def __init__(self, content, *args, **kwargs):
        encoded = json.dumps(content)
        super(JSONResponse, self).__init__(content=encoded, mimetype='application/json; charset=utf-8')

def lookup_by_md5_prefix(request, md5_prefix):
    """
    Finds outputs an object with two keys: 'worse' and 'better'.
    The 'worse' value is a list of URLs that the given MD5 prefix is worse then.
    The 'better' value is a list of URLs that the given MD5 prefix is better than.
    """
    if request.GET.get('only_better') not in TRUTH_STRINGS:
        worse_edges = Edge.objects.filter(better_md5__startswith=md5_prefix)
    else:
        worse_edges = []


    if request.GET.get('only_worse') not in TRUTH_STRINGS:
        better_edges = Edge.objects.filter(worse_md5__startswith=md5_prefix)
    else:
        better_edges = []

    better_urls = [b.better_url for b in better_edges]
    worse_urls = [w.worse_url for w in worse_edges]
    result = {
        'better': better_urls,
        'worse': worse_urls
    }
    return JSONResponse(result)

def graph_from_md5(request, md5):
    raise Exception('Not implemented yet.')
