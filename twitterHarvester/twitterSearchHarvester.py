from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API, Cursor
import numpy as np
import pandas as pd

from tweeter_credential import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

MELBOURNE_GEO_CODE = "-37.813628,144.963058"


class TweeterSearchHarvester:
    """
    Return tweets using a query string.
    """

    def __init__(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = api = API(auth)

    def get_tweets(self, query, max_tweets=5, center=MELBOURNE_GEO_CODE, radius="20km"):
        """
        Parameters
        --------------
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
        searched_tweets = [status for status in Cursor(
            self.api.search, q=query, geocode=geocode).items(max_tweets)]

        return searched_tweets


def make_df_from_tweets(tweets):
    df = pd.DataFrame(
        data=[tweet.text for tweet in tweets], columns=['tweets'])

    df["user location"] = np.array(
        [tweet._json['user']['location'] for tweet in tweets])
    df['id'] = np.array([tweet.id for tweet in tweets])
    df['len'] = np.array([len(tweet.text) for tweet in tweets])
    df['date'] = np.array([tweet.created_at for tweet in tweets])
    df['source'] = np.array([tweet.source for tweet in tweets])
    df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
    df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

    return df


if __name__ == "__main__":
    tweet_getter = TweeterSearchHarvester()

    query = 'I wish'

    tweets = tweet_getter.get_tweets(query, max_tweets=100)

    tweets_df = make_df_from_tweets(tweets)

    csv_file_name_to_save = 'test.csv'

    tweets_df.to_csv(csv_file_name_to_save)
