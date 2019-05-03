
from tweepy import OAuthHandler
from tweepy import API, Cursor, RateLimitError
import numpy as np
import pandas as pd
from utils import make_df_from_tweets
import time
import json
import sys


from twitter_credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


# geocode :Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile.
# to get the coordicates :  https://google-developers.appspot.com/maps/documentation/utils/geocoder/
MELBOURNE_GEO_CODE = "-37.813628,144.963058"
SYDNEY_GEO_CODE = "-33.86882,151.209296"
BRISBANE_GEO_CODE = " -27.469771,153.025124"
GEELONG_GEO_CODE = "-38.149918,144.361719"


class TweeterSearchHarvester:
    """
    Return tweets using a query string.
    """

    def __init__(self, file_for_tweets):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = API(auth)
        self.limited_chuck_size = 1600  # should be set to around 1600
        self.file_for_tweets = file_for_tweets

    def resetConnection(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = API(auth)

    def get_tweets(self, query, n_periods, current_count, wanted_amount=5, center=MELBOURNE_GEO_CODE, radius="100km"):
        """
        Parameters
        --------------
        max_tweets:
            number of tweets want to extract.
        query:
            search query of 500 characters maximum, including operator.

            More about operator
            refers to https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators

        geocode : latitude,longitude,radius
            radius units must be specified as either " mi " (miles) or " km " (kilometers).

        Returns:
        -------------
        List of tweet:
            tweet: tweepy.models.Status

        """
        geocode = center + "," + radius
        # searched_tweets = [status for status in Cursor(
        #     self.api.search, q=query, geocode=geocode).items()]
        searched_tweets = []
        max_id = None

        while len(searched_tweets) <= wanted_amount:
            if len(searched_tweets) == 0:
                try:
                    tweets = self.api.search(
                        q=query, geocode=geocode, count=100)
                except RateLimitError:
                    print("Shold sleep")
                    time.sleep(60 * 15)

                    self.resetConnection()
            else:
                tweets = self.api.search(
                    q=query, geocode=geocode, count=100, max_id=max_id-1)

            if len(tweets) == 0:
                break
            searched_tweets += tweets

            max_id = tweets[-1]._json['id']

            # can store tweet into the database here or write into a file.
            with open(self.file_for_tweets, 'a+') as f:
                for tweet in tweets:
                    dat = tweet._json
                    dat['method'] = "searchAPI" + "_" + "melbourne"
                    f.write(json.dumps(dat) + "\n")

            if len(searched_tweets) + current_count >= n_periods * self.limited_chuck_size:
                print("take a break")
                time.sleep(10)  # should be set to 15 mins
                n_periods += 1

        new_count = len(searched_tweets) + current_count
        return searched_tweets, new_count, n_periods, max_id


def extractTweets(queries, file_to_save, location_center=MELBOURNE_GEO_CODE, radius="100km"):

    tweet_getter = TweeterSearchHarvester(
        file_for_tweets=file_to_save)

    n_periods = 1
    current_count = 0

    total_tweets = []

    key_word_max_ids = {}

    for query in queries:

        tweets, current_count, n_periods, key_word_max_id = tweet_getter.get_tweets(
            query, wanted_amount=1500, center=location_center, radius=radius, n_periods=n_periods, current_count=current_count)

        key_word_max_ids[query] = key_word_max_id

        for tweet in tweets:
            total_tweets.append(tweet._json)

        print(current_count)
        print(n_periods)

    # tweets = [t._json for t in tweets]

    # tweets_df = make_df_from_tweets(total_tweets)

    # tweets_df.to_csv('test.csv')

    return key_word_max_ids


if __name__ == "__main__":

    queries = ["Auspol", "labor", "liberal", "greens",
               "united australia party", "GRN", "ALP", "LNP", "election", "vote",
               "Scott morrison", "bill shorten"]

    location = sys.argv[1]
    if location == "sydney":
        file_to_save = "sydney_search_json"
        center = SYDNEY_GEO_CODE
    elif location == 'melbourne':
        file_to_save = "melbourne_search_json"
        center = MELBOURNE_GEO_CODE
    elif location == "brisbane":
        file_to_save = "brisbane_search_json"
        center = BRISBANE_GEO_CODE
    elif location == "geelong":
        file_to_save = "geelong_search_json"
        center = GEELONG_GEO_CODE

    # queries = ["Auspol", "labor", "liberal"]
    key_word_max_ids = extractTweets(
        queries, file_to_save, location_center=location, radius="100km")

    with open("key_word_ids.json", "a") as f:
        f.write(json.dumps(key_word_max_ids) + "\n")

