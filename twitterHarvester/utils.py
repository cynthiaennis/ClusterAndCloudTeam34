import pandas as pd
import numpy as np
import json
import re





def make_df_from_tweets(tweets):
    """
    Params
    -------------------------
    tweets : list of jsons

    Returns
    -------------------------
    pd.Dataframe
    """
    df = pd.DataFrame(
        data=[tweet['text'] for tweet in tweets], columns=['tweets'])
    df['screen_name'] = np.array(
        [tweet['user']["screen_name"] for tweet in tweets])
    df["user_id"] = np.array(
        [tweet['user']['id'] for tweet in tweets])
    df["user_location"] = np.array(
        [tweet['user']['location'] for tweet in tweets])
    df['id'] = np.array([tweet['id'] for tweet in tweets])
    df['len'] = np.array([len(tweet['text']) for tweet in tweets])
    df['date'] = np.array([tweet['created_at'] for tweet in tweets])
    df['source'] = np.array(
        [re.sub('<[^<]+?>', '', tweet['source']) for tweet in tweets])
    df['likes'] = np.array([tweet['favorite_count'] for tweet in tweets])
    df['retweets'] = np.array([tweet['retweet_count'] for tweet in tweets])
    df['coor'] = np.array([tweet["coordinates"] for tweet in tweets])

    df['hashtags'] = np.array([tweet['entities']['hashtags']
                               for tweet in tweets])
    return df
