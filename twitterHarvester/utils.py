
from textblob import TextBlob
import json
import re
import math


POLITICAL_KEY_WORDS = ["Auspol", "labor", "liberal", "greens",
                       "united australia party", "GRN", "ALP", "LNP", "election", "vote",
                       "Scott morrison", "bill shorten"]


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


def is_negative_sentiment(text):

    blob = TextBlob(text)

    score = blob.sentiment.polarity

    if score < 0:
        return 1
    else:
        return 0


def is_bounded_by(coords, bounds):
    """
    bounds:
         direct copy from google.
         [[north , west],[south ,east] ]
         [[max_lat , max_long]  , [min_lat , min_long] ]
         melbourne lat long is -37 , 144
    coord:
          [longitude, latitude].

           "coordinates": {
                "type": "Point",
                "coordinates": [
                  151.02,
                  -33.86
                ]
              }
    """
    min_lat = bounds[1][0]
    min_long = bounds[1][1]

    max_lat = bounds[0][0]
    max_long = bounds[0][1]

    target_lat = coords[1]
    target_long = coords[0]

    if target_lat >= min_lat and target_lat <= max_lat:
        if target_long >= min_long and target_long <= max_long:
            return True

    return False


def is_political(text):

    text = text.lower()
    for word in POLITICAL_KEY_WORDS:
        if word.lower() in text:

            return True

    return False
