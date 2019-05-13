
from tweepy import OAuthHandler
from tweepy import API, Cursor, RateLimitError
import time
import json
import sys
import couchdb


import high_income_cities_coordinates as hc
import low_income_cities_coordinates as lc


from utils import calculate_radius, find_box_center, is_negative_sentiment
from twitter_credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


# geocode :Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile.
# to get the coordicates :  https://google-developers.appspot.com/maps/documentation/utils/geocoder/
MELBOURNE_GEO_CODE = "-37.813628,144.963058"
# SYDNEY_GEO_CODE = "-33.86882,151.209296"
# BRISBANE_GEO_CODE = " -27.469771,153.025124"
# GEELONG_GEO_CODE = "-38.149918,144.361719"

db_tweet_name = 'new_twitter_search'
db_user_name = 'admin'
db_password = "admin"

db_address = "http://%s:%s@172.26.38.116:5984/" % (db_user_name, db_password)
db_server = couchdb.Server(db_address)
if db_tweet_name in db_server:
    db_tweet = db_server[db_tweet_name]
else:
    db_tweet = db_server.create(db_tweet_name)


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
                    try:
                        tweets = self.api.search(
                            q=query, geocode=geocode, count=100, max_id=max_id-1)
                    except Exception as e:
                        print(e)
                        time.sleep(10)
                        tweets = []
            except RateLimitError:
                print("Shold sleep")
                time.sleep(60 * 15)

                self.resetConnection()

            if len(tweets) == 0:
                break
            searched_tweets += tweets

            max_id = tweets[-1]._json['id']

            # can store tweet into the database here or write into a file.
            # with open(self.file_for_tweets, 'a+') as f:
            #     for tweet in tweets:
            #         dat = tweet._json
            #         dat['method'] = "searchAPI_" + place_name
            #         f.write(json.dumps(dat) + "\n")
            #         print("adding " + dat["id_str"])
            for tweet in tweets:
                dat = tweet._json
                dat['method'] = "searchAPI_" + place_name
                dat["tweet_location"] = place_name
                dat['is_gegative_sentiment'] = is_negative_sentiment(
                    dat['text'])
                try:

                    db_tweet[dat["id_str"]] = {"tweet": dat}
                except Exception as e:
                    print(e)
                    pass

                print("adding " + dat["id_str"])

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
            query, wanted_amount=6000, center=location_center, radius=radius, n_periods=n_periods, current_count=current_count, place_name=place_name)

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
               "united australia party", 'UAP', "GRN", "ALP", "LNP", "election", "vote",
               "Scott morrison", "bill shorten", "UnitedAusParty", "CliveFPalmer",
               "Clive Palmer"]

    map_to_coor = {"bundaberg": lc.Bundaberg,
                   "sydney": hc.Sydney, "ACT": hc.ACT, "randwick": hc.Randwick,
                   "stirling": hc.Stirling, "townsville": hc.Townsville, "boroondara": hc.Boroondara,
                   "greater_dandenong": lc.Greater_Dandenong, "coffs_harbour": lc.Coffs_Harbour,
                   "shoalhaven": lc.Shoalhaven, "lismore": lc.Lismore, "fraser_coast": lc.Fraser_Coast, "mosman": hc.Mosman, "north_sydney": hc.North_Sydney,
                   "lane_cove": hc.Lane_cove,
                   "tweed": lc.Tweed, "noosa": lc.Noosa,
                   "port_macquaire_hastings": lc.Port_Macquarie_Hastings,
                   "gympie": lc.Gympie,
                   "ballina": lc.Ballina,
                   "cunberland": lc.Cumberland,
                   "sunshine_coast": lc.Sunshine_Coast,
                   "burwoord": lc.Burwood,
                   "devonport": lc.Devonport,
                   "lockyer_valley": lc.Lockyer_Valley,
                   "eurobodalla": lc.Eurobodalla,
                   "greater_shepparton": lc.Greater_Shepparton,
                   "mildura": lc.Mildura,
                   "east_gippsland": lc.East_Gippsland,
                   "moonee_valley": hc.Moonee_Valley,
                   "stonnington": hc.Stonnington,
                   "woollahra": hc.Woollahra,
                   "nedlands": hc.Nedlands,
                   "port_phillip": hc.Port_Phillip,
                   "darwin": hc.Darwin,
                   "yarra": hc.Yarra,
                   "inner_west": hc.Inner_West,
                   "ku_ring_gai": hc.Ku_ring_gai,
                   "waverley": hc.Waverley,
                   "glen_eira": hc.Glen_Eira,
                   "bass_coast": lc.Bass_Coast
                   }

    for location in map_to_coor.keys():

        location_coor = map_to_coor[location]

        center = find_box_center(location_coor[0], location_coor[1])

        R = calculate_radius(location_coor[0], location_coor[1])

        file_to_save = "search.json"

        extractTweets(queries=queries, file_to_save=file_to_save,
                      location_center=center, radius=R, place_name=location)

    # for location in low_income_areas:

    #     location_coor = map_to_coor[location]

    #     center = find_box_center(location_coor[0], location_coor[1])

    #     R = calculate_radius(location_coor[0], location_coor[1])

    #     file_to_save = "search.json"

    #     extractTweets(queries=queries, file_to_save=file_to_save,
    #                   location_center=center, radius=R, place_name=location)
