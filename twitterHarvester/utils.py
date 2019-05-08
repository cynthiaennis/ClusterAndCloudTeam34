import pandas as pd
import numpy as np
import json
import re
import math


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


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


def find_box_center(north_east, south_west):

    p1 = (north_east[0] + south_west[0]) / 2

    p2 = (north_east[1] + south_west[1]) / 2

    return (p1, p2)


def calculate_radius(north_east, south_west):
    """
    Boundaries are from https://google-developers.appspot.com/maps/documentation/utils/geocoder/

    """

    center = find_box_center(north_east, south_west)

    return distance(center, south_west)
