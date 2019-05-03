from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API, Cursor

import twitter_credentials

MELBOURNE_BOUNDARIES = [144.593742, -38.433859,  145.512529, -37.511274]
SYDNEY_BOUNDARIES = [150.520929, -34.118347, 151.343021, -33.578141]


class TweeterListener(StreamListener):
    """
    Given a file name to store the tweet data.
    """

    def __init__(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self, data):

        try:
            print(data)
            with open(self.fetched_tweet_filename, 'a+') as f:
                f.write(data)
            return True
        except BaseException as e:
            print("Error on_data {}".format(e))
            return True

    def on_error(self, status):
        if status == 420:
            return False
        print(status)


class TweeterStreamer:
    """
    Class for streaming and processing live tweet.

    Parameters:
        auth_handler – authentication handler to be used
        host – general API host
        search_host – search API host
        cache – cache backend to use
        api_root – general API path root
        search_root – search API path root
        retry_count – default number of retries to attempt when error occurs
        retry_delay – number of seconds to wait between retries
        retry_errors – which HTTP status codes to retry
        timeout – The maximum amount of time to wait for a response from Twitter
        parser – The object to use for parsing the response from Twitter
        compression – Whether or not to use GZIP compression for requests
        wait_on_rate_limit – Whether or not to automatically wait for rate limits to replenish
        wait_on_rate_limit_notify – Whether or not to print a notification when Tweepy is waiting for rate limits to replenish
        proxy – The full url to an HTTPS proxy to use for connecting to Twitter.

    """

    def __init__(self, location_bounds):

        self.auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                                 twitter_credentials.CONSUMER_SECRET)

        self.auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                                   twitter_credentials.ACCESS_TOKEN_SECRET)

        self.location_bounds = location_bounds

    def stream_tweet(self, file_name_to_save):
        listener = TweeterListener(file_name_to_save)

        stream = Stream(self.auth, listener)
        #  locations=[-38, 144, -37, 146]
        # locations=[144.593742, -38.433859,  145.512529, -37.511274]
        stream.filter(locations=self.location_bounds, is_async=True)


if __name__ == '__main__':

    melbourne_file = 'melbourne_stream.json'

    melbroune_streamer = TweeterStreamer(MELBOURNE_BOUNDARIES)
    melbroune_streamer.stream_tweet(melbourne_file)

    sydney_file = 'sydney_sydney.json'
    sydney_streamer = TweeterStreamer(SYDNEY_BOUNDARIES)
    sydney_streamer.stream_tweet(sydney_file)
