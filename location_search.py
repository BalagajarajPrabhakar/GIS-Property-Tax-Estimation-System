from geopy.distance import geodesic


def find_nearest_property(lat,lon,data):

    clicked = (lat,lon)

    nearest=None
    min_distance=float("inf")

    for _,row in data.iterrows():

        property_loc=(row["latitude"],row["longitude"])

        distance=geodesic(clicked,property_loc).meters

        if distance<min_distance:

            min_distance=distance
            nearest=row

    return nearest