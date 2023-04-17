from src.infra.cost_of_living_scraper import scrape_data_from_website
from src.infra.get_geo_data import get_lat_lon_for_cities


def main():
    df_cost_of_living = scrape_data_from_website()
    df_cost_of_living.to_csv('https://github.com/gjuresic/cost_of_living_german_cities/blob/main/src/data/'
                             'cost_of_living_data.csv')

    df_geo_data = get_lat_lon_for_cities()
    df_geo_data.to_csv('https://github.com/gjuresic/cost_of_living_german_cities/blob/main/src/data/geo_data.csv')


if __name__ == '__main__':
    main()
