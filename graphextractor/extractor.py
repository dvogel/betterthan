from graphextractor.tweetparser import TweetLexer, TweetParser
from graphextractor.models import Edge, Topic


def parse_tweet_text(tweet_text):
    """
    Attempts to parse the text of the given tweet (model or model pk).
    It returns a 2-tuple of type (True, dict) if the text was parsed
    successfully and (False, Exception) if the text was not parseable.
    """
    token_stream = TweetLexer.lex(tweet_text)
    try:
        parsed = TweetParser.parse(token_stream)
        return (True, parsed)
    except ValueError as err:
        return (False, err)


def extract_edge_from_tweet_text(tweet_text):
    (parsed_ok, result) = parse_tweet_text(tweet_text)
    if parsed_ok:
        edge = Edge.for_urls(worse_url=result['worse_url'],
                             better_url=result['better_url'])

        for topic_name in result['topics']:
            (topic, created) = Topic.objects.get_or_create(name=topic_name)
            edge.topics.add(topic)

        return edge

    else:
        raise result

    
