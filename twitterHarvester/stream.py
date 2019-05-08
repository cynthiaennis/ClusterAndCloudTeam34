import tweepy
from urllib3.exceptions import ProtocolError
from twitter_credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import json
import couchdb
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


# consumer key, consumer secret, access token, access secret.
ckey = CONSUMER_KEY
csecret = CONSUMER_SECRET
atoken = ACCESS_TOKEN
asecret = ACCESS_TOKEN_SECRET

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)
db_tweet_name = 'tweet'
db_user_name = 'user'
db_address = "http://localhost:5984/"
db_server = couchdb.Server(db_address)

if db_tweet_name in db_server:
    db_tweet = db_server[db_tweet_name]
else:
    db_tweet = db_server.create(db_tweet_name)

if db_user_name in db_server:
    db_user = db_server[db_user_name]
else:
    db_user = db_server.create(db_user_name)

bounding_box = [110.951034, -54.833766, 159.287222, -9.187026]


class listener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        doc_id = tweet["id_str"]
        if doc_id not in db_tweet:
            db_tweet[doc_id] = {"tweet": tweet}
        print("new tweet: "+doc_id)
        if tweet["user"]["id_str"] not in db_user:
            try:
                for status in tweepy.Cursor(api.user_timeline, screen_name=tweet["user"]["screen_name"], tweet_mode='extended').items():
                    user_tweet = status._json
                    if user_tweet["coordinates"] is not None:
                        if bounding_box[2] > user_tweet["coordinates"]["coordinates"][0] > bounding_box[0] \
                                and bounding_box[3] > user_tweet["coordinates"]["coordinates"][1] > bounding_box[1]:
                            doc_id = user_tweet["id_str"]
                            if doc_id not in db_tweet:
                                db_tweet[doc_id] = {"tweet": tweet}
                                print("new tweet: "+doc_id)
                db_user[tweet["user"]["id_str"]] = {"complete": "y"}
                print("user: "+tweet["user"]["id_str"]+" completed")
            except Exception as e:
                print(e)
                pass
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
