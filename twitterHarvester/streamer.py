import tweepy
from urllib3.exceptions import ProtocolError
from Twitter_Credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import json
import couchdb
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import utils
import high_income_cities_coordinates as hc
import low_income_cities_coordinates as lc


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

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

db_tweet_name = 'new_twitter_search'

db_user_name = 'admin'
db_password = "admin"

db_address = "http://%s:%s@172.26.38.116:5984/" % (db_user_name, db_password)
db_server = couchdb.Server(db_address)

if db_tweet_name in db_server:
    db_tweet = db_server[db_tweet_name]
else:
    db_tweet = db_server.create(db_tweet_name)



bounding_box = [110.951034, -54.833766, 159.287222, -9.187026]


def check_tweet(tweet):
    try:
        if tweet["coordinates"] is not None:
            for location in map_to_coor.keys():

                # If is in any location of interest
                boundary = map_to_coor[location]
                if utils.is_bounded_by(tweet["coordinates"]["coordinates"], boundary):
                    if utils.is_political(tweet['text']):
                        tweet["tweet_location"] = location

                        tweet['is_gegative_sentiment'] = utils.is_negative_sentiment(
                            tweet['text'])

                        # save to database here.
                        db_tweet[tweet['id_str']] = {"tweet": tweet}
                        print("new tweet: "+tweet["id_str"])
    except:
        pass


class listener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        doc_id = tweet["id_str"]
        print(doc_id)
        if doc_id not in db_tweet:
            check_tweet(tweet)
            # db_tweet[doc_id] = {"tweet": tweet}

        # Check user_id in database.
        # if tweet["user"]["id_str"] not in db_user:
        #     try:
        #         for status in tweepy.Cursor(api.user_timeline, screen_name=tweet["user"]["screen_name"], tweet_mode='extended').items():
        #             user_tweet = status._json
        #             check_tweet(user_tweet)

        #         db_user[tweet["user"]["id_str"]] = {"complete": "y"}
        #         print("user: "+tweet["user"]["id_str"]+" completed")

        #         # Write to the file or save to the DB.
        #     except Exception as e:
        #         print(e)
        #         pass
        return True

    def on_error(self, status):
        print(status)

    def on_exception(self, exception):
        print(exception)
        return


def tweet_to_json(tweet):
    tweet_dict = {
        "text": json.loads(tweet)['text'],
        "author_name": json.loads(tweet)['user']['screen_name']
    }
    with open('tweet.json', 'a+') as f:
        json.write(tweet_dict, f)


myStreamListener = listener()
myStream = Stream(auth=api.auth, listener=myStreamListener)

while True:
    try:
        myStream.filter(locations=bounding_box)
    except ProtocolError:
        continue
