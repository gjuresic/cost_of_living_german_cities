import opencage.geocoder
import pandas as pd


def get_lat_lon_for_cities():
    geocoder = opencage.geocoder.OpenCageGeocode("API-KEY")

    cities = ['Munich', 'Stuttgart', 'Karlsruhe', 'Heidelberg', 'Mannheim', 'Nuremberg', 'Darmstadt', 'Frankfurt',
              'Dresden', 'Leipzig', 'Berlin', 'Hanover', 'Bremen', 'Hamburg', 'Aachen', 'Bonn', 'Cologne', 'Dusseldorf',
              'Essen', 'Dortmund']

    latitudes = []
    longitudes = []

    for city in cities:
        result = geocoder.geocode(city)
        lat = result[0]['geometry']['lat']
        lon = result[0]['geometry']['lng']
        latitudes.append(lat)
        longitudes.append(lon)

    df = pd.DataFrame({"city": cities, "lat": latitudes, "lon": longitudes})

    return df
