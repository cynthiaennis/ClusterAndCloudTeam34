from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API, Cursor
import numpy as np
import pandas as pd
from utils import make_df_from_tweets
import time
import json
from random import sample

from twitter_credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# to get the coordicates :  https://google-developers.appspot.com/maps/documentation/utils/geocoder/
MELBOURNE_GEO_CODE = "-37.813628,144.963058"
SYDNEY_GEO_CODE = "-33.86882,151.209296"
BRISBANE_GEO_CODE = " -27.469771,153.025124"


class TweeterUserTracker:
    """
    Return tweets using a query string.
    """

    def __init__(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = API(auth)
        self.limited_chuck_size = 1500  # should be set to around 1600

    def get_past_tweets(self, screen_name, count=200):
        """
        parameters:
          screen_name: user's twitter screen_name.
          count: number of past tweets wish to extract.

        return:
          tweets: list of tweets. each tweets is a python dictionary.
        """
        if count <= 200:
            return self.api.user_timeline(screen_name=screen_name, count=count)

        else:
            total_tweets = []
            tweets = self.api.user_timeline(
                screen_name=screen_name, count=count)

            total_tweets += tweets
            max_id = tweets[-1]._json['id']

            while(len(total_tweets) < count):
                tweets = self.api.user_timeline(
                    screen_name=screen_name, count=count, max_id=max_id - 1)
                if len(tweets) == 0:
                    return total_tweets
                else:
                    total_tweets += tweets
                    max_id = tweets[-1]._json['id']


if __name__ == "__main__":
    tweet_getter = TweeterUserTracker()

    total_tweets = []

    users = []

    file_to_read = "melborune_json.json"

    # file to write the tweets from user pass tweets
    user_file_to_save = "melbourne_user.json"
    seem_users = set()

    N = 1500
    # randomly sample N user to track.
    with open(file_to_read, 'r') as f:

        lines = f.readlines()
        N = len(lines)
        while(len(seem_users) <= 3000):

            i = sample(range(N), 1)[0]

            line = lines[i]
            data = json.loads(line.rstrip())

            user = data['user']['screen_name']

            if not user in seem_users:
                seem_users.add(user)
                print(user)

                tweets = tweet_getter.get_past_tweets(screen_name=user)

                total_tweets += [t._json for t in tweets]

                print(len(total_tweets))

                with open(user_file_to_save, 'a+') as f:
                    for tweet in tweets:
                        dat = tweet._json
                        dat['method'] = "searchAPI" + \
                            "_" + "melbourne" + "track_user"
                        f.write(json.dumps(dat) + "\n")

    # tweets_df = make_df_from_tweets(total_tweets)

    # tweets_df.to_csv('user2.csv')
