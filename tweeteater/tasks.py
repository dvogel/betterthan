from __future__ import print_function

import os
import logging

Log = logging.getLogger(os.path.basename(__file__)
                        if __name__ == "__main__"
                        else __name__)

def log_tweet(tweet):
    Log.info("Ate tweet from {u}: {t}".format(u=tweet.user.screen_name, t=tweet.text))

def echo_tweet(tweet):
    print("Ate tweet from {u}: {t}".format(u=tweet.user.screen_name, t=tweet.text))
