
from tweepy import OAuthHandler
from tweepy import API, Cursor, RateLimitError
# import numpy as np
# import pandas as pd
from utils import make_df_from_tweets
import time
import json
import sys
# import couchdb


from low_income_cities_coordinates import Greater_Dandenong, Coffs_Harbour, Shoalhaven, Lismore, Fraser_Coast
from high_income_cities_coordinates import Sydney, Stirling, Townsville, Boroondara, Randwick, ACT
from utils import calculate_radius, find_box_center
from twitter_credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


# geocode :Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile.
# to get the coordicates :  https://google-developers.appspot.com/maps/documentation/utils/geocoder/
# MELBOURNE_GEO_CODE = "-37.813628,144.963058"
# SYDNEY_GEO_CODE = "-33.86882,151.209296"
# BRISBANE_GEO_CODE = " -27.469771,153.025124"
# GEELONG_GEO_CODE = "-38.149918,144.361719"


# db_tweet_name = "search_api_tweets"
# db_user_name = 'user'
# db_address = "http://localhost:5984/"
# db_server = couchdb.Server(db_address)

# if db_tweet_name in db_server:
#     db_tweet = db_server[db_tweet_name]
# else:
#     db_tweet = db_server.create(db_tweet_name)

# if db_user_name in db_server:
#     db_user = db_server[db_user_name]
# else:
#     db_user = db_server.create(db_user_name)


class TweeterSearchHarvester:
    """
    Return tweets using a query string.
    """

    def __init__(self, file_for_tweets):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = API(auth, wait_on_rate_limit=True)
        self.limited_chuck_size = 5500  # should be set to around 1600
        self.file_for_tweets = file_for_tweets

    def resetConnection(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = API(auth)

    def get_tweets(self, query, n_periods, current_count, place_name, wanted_amount=5, center=MELBOURNE_GEO_CODE, radius="100km"):
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
        geocode = None
        if type(center) == tuple:
            center = str(center[0]) + ","+str(center[1])
        else:
            geocode = center + "," + radius
        # searched_tweets = [status for status in Cursor(
        #     self.api.search, q=query, geocode=geocode).items()]
        searched_tweets = []
        max_id = None

        while len(searched_tweets) <= wanted_amount:
            try:
                if len(searched_tweets) == 0:

                    tweets = self.api.search(
                        q=query, geocode=geocode, count=100)

                else:
                    tweets = self.api.search(
                        q=query, geocode=geocode, count=100, max_id=max_id-1)

            except RateLimitError:
                print("Shold sleep")
                time.sleep(60 * 15)

                self.resetConnection()

            if len(tweets) == 0:
                break
            searched_tweets += tweets

            max_id = tweets[-1]._json['id']

            # can store tweet into the database here or write into a file.
            with open(self.file_for_tweets, 'a+') as f:
                for tweet in tweets:
                    dat = tweet._json
                    dat['method'] = "searchAPI_" + place_name
                    f.write(json.dumps(dat) + "\n")
                    print("adding " + dat["id_str"])
            # for tweet in tweets:
            #     dat = tweet._json
            #     dat['method'] = "searchAPI_" + place_name
            #     try:
            #         db_search[dat["id_str"]] = {"tweet": dat}
            #     except Exception as e:
            #         print(e)
            #         pass

            #     print("adding " + dat["id_str"])

            if len(searched_tweets) + current_count >= n_periods * self.limited_chuck_size:
                print("take a break")
                time.sleep(60 * 5)  # should be set to 15 mins
                n_periods += 1

        new_count = len(searched_tweets) + current_count
        return searched_tweets, new_count, n_periods, max_id


def extractTweets(queries, file_to_save, place_name, location_center=MELBOURNE_GEO_CODE, radius="100km"):
    """
    file_to_save: json file you want save the tweets.
    """
    tweet_getter = TweeterSearchHarvester(
        file_for_tweets=file_to_save)

    n_periods = 1
    current_count = 0

    total_tweets = []

    key_word_max_ids = {}

    for query in queries:

        tweets, current_count, n_periods, key_word_max_id = tweet_getter.get_tweets(
            query, wanted_amount=1500, center=location_center, radius=radius, n_periods=n_periods, current_count=current_count, place_name=place_name)

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

    high_income_areas = ["ACT", "randwick",
                         "stirling", "townsville", "boroondara"]

    low_income_areas = ["greater_dandenong", "coffs_harbour", "shoalhaven",
                        "lismore", "fraser_coast"]

    map_to_coor = {"sydney": Sydney, "ACT": ACT, "randwick": Randwick,
                   "stirling": Stirling, "townsville": Townsville, "boroondara": Boroondara,
                   "greater_dandenong": Greater_Dandenong, "coffs_harbour": Coffs_Harbour,
                   "shoalhaven": Shoalhaven, "lismore": Lismore, "fraser_coast": Fraser_Coast}

    for location in high_income_areas:

        location_coor = map_to_coor[location]

        center = find_box_center(location_coor[0], location_coor[1])

        R = calculate_radius(location_coor[0], location_coor[1])

        file_to_save = "search.json"

        extractTweets(queries=queries, file_to_save=file_to_save,
                      location_center=center, radius=R, place_name=location)

    for location in low_income_areas:

        location_coor = map_to_coor[location]

        center = find_box_center(location_coor[0], location_coor[1])

        R = calculate_radius(location_coor[0], location_coor[1])

        file_to_save = "search.json"

        extractTweets(queries=queries, file_to_save=file_to_save,
                      location_center=center, radius=R, place_name=location)
