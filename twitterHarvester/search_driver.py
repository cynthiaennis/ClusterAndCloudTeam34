
from searcher import extractTweets
from low_income_cities_coordinates import Greater_Dandenong, Coffs_Harbour, Shoalhaven, Lismore, Fraser_Coast

from high_income_cities_coordinates import Sydney, Stirling, Townsville, Boroondara, Randwick, ACT

from utils import calculate_radius, find_box_center

queries = ["Auspol", "labor", "liberal", "greens",
           "united australia party", "GRN", "ALP", "LNP", "election", "vote",
           "Scott morrison", "bill shorten"]


file_to_save = "fraser_coast_search.json"

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

    # file_to_save = location + "_search.json"

    extractTweets(queries=queries, file_to_save=file_to_save,
                  location_center=center, radius=R, place_name=location)

for location in low_income_areas:

    location_coor = map_to_coor[location]

    center = find_box_center(location_coor[0], location_coor[1])

    R = calculate_radius(location_coor[0], location_coor[1])

    # file_to_save = location + "_search.json"

    extractTweets(queries=queries, file_to_save=None,
                  location_center=center, radius=R, place_name=location)
