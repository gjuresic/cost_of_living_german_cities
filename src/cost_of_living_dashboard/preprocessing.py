import pandas as pd
import numpy as np


def get_df():
    df = pd.read_csv('/Users/gjuresic/Desktop/python_projects/cost_of_living_german_cities/src/'
                     'data/cost_of_living_data.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df['price'] = df['price'].replace('?', np.nan).str.replace(',', '').astype(float)
    df['min_price'] = df['min_price'].replace('?', np.nan).str.replace(',', '').astype(float)
    df['max_price'] = df['max_price'].replace('?', np.nan).str.replace(',', '').astype(float)
    df['price'].fillna(0, inplace=True)
    df['inserted_at'] = pd.Timestamp.today().strftime("%B %d, %Y")

    df_geo = pd.read_csv('/Users/gjuresic/Desktop/python_projects/cost_of_living_german_cities/src/data/geo_data.csv')
    df = pd.merge(df, df_geo, how='left', left_on=['city'], right_on=['city'])
    df['category'] = df['category'].replace('Apartment (3 bedrooms)', 'Buy Apartment')
    df['category'] = df['category'].replace('Internet (60 Mbps', 'Sports And Leisure')

    return df


def merge_dfs(df):
    city_list = np.sort(df['city'].unique().tolist())
    df_city_list = []
    for city in city_list:
        df_city = df[df.city == city]
        df_city.reset_index(inplace=True)
        df_city = df_city[['price']]
        df_city.rename(columns={'price': city}, inplace=True)
        df_city_list.append(df_city)

    df_merged = pd.concat(df_city_list, axis=1)

    for i, city1 in enumerate(city_list):
        for city2 in city_list[i + 1:]:
            col_diff = f'Difference: {city1} - {city2}'
            df_merged[col_diff] = ((df_merged[city1] - df_merged[city2]) / df_merged[city1])

    df_merged = df_merged[[city for city in city_list] +
                          [f'Difference: {city1} - {city2}' for i, city1 in enumerate(city_list)
                           for city2 in city_list[i + 1:]]]
    df_merged = df_merged.round(2)
    df_help = df[df.city == 'Munich']
    df_help.reset_index(inplace=True)
    df_help = df_help[['category', 'property']]
    df_merged = pd.concat([df_merged, df_help], axis=1)

    df_merged['weight'] = float('nan')
    df_merged.loc[df_merged['property'] == 'Milk (regular), (1 liter)', 'weight'] = 20
    df_merged.loc[df_merged['property'] == 'Loaf of Fresh White Bread (500g)', 'weight'] = 8
    df_merged.loc[df_merged['property'] == 'Local Cheese (1kg)', 'weight'] = 3
    df_merged.loc[df_merged['property'] == 'Beef Round (1kg) (or Equivalent Back Leg Red Meat)', 'weight'] = 4
    df_merged.loc[df_merged['property'] == 'Apples (1kg)', 'weight'] = 10
    df_merged.loc[df_merged['property'] == 'Banana (1kg)', 'weight'] = 6
    df_merged.loc[df_merged['property'] == 'Tomato (1kg)', 'weight'] = 15
    df_merged.loc[df_merged['property'] == 'Potato (1kg)', 'weight'] = 6
    df_merged.loc[df_merged['property'] == 'Lettuce (1 head)', 'weight'] = 20
    df_merged.loc[df_merged['property'] == 'Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)', 'weight'] = 2
    df_merged['weight'].fillna(1, inplace=True)

    return df_merged


def get_selected_properties():
    selected_properties = ['Meal for 2 People, Mid-range Restaurant, Three-course', 'Milk (regular), (1 liter)',
                           'Loaf of Fresh White Bread (500g)', 'Rice (white), (1kg)', 'Eggs (regular) (12)',
                           'Local Cheese (1kg)', 'Beef Round (1kg) (or Equivalent Back Leg Red Meat)',
                           'Apples (1kg)',
                           'Banana (1kg)', 'Oranges (1kg)', 'Tomato (1kg)', 'Potato (1kg)', 'Onion (1kg)',
                           'Lettuce (1 head)', 'Bottle of Wine (Mid-Range)', 'Monthly Pass (Regular Price)',
                           'Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)',
                           'Fitness Club, Monthly Fee for 1 Adult',
                           'Cinema, International Release, 1 Seat', 'Apartment (1 bedroom) in City Centre']
    return selected_properties


def get_overall_costs(df_merged):
    city_one = 'Aachen'
    city_two = 'Berlin'
    selected_properties = get_selected_properties()
    df_copy = df_merged.copy(deep=True)
    df_copy_city_one = df_copy[['property', 'weight', city_one]]
    df_selected_city_one = df_copy_city_one.loc[df_copy_city_one['property'].isin(selected_properties)]
    df_selected_city_one['weighted_price'] = df_selected_city_one[city_one] * df_selected_city_one['weight']
    weighted_sum_city_one = round(df_selected_city_one['weighted_price'].sum(), 0)

    df_copy_city_two = df_copy[['property', 'weight', city_two]]
    df_selected_city_two = df_copy_city_two.loc[df_copy_city_two['property'].isin(selected_properties)]
    df_selected_city_two.fillna(1, inplace=True)
    df_selected_city_two['weighted_price'] = df_selected_city_two[city_two] * df_selected_city_two['weight']
    weighted_sum_city_two = round(df_selected_city_two['weighted_price'].sum(), 0)

    df_all_costs = pd.DataFrame({'City': [city_one, city_two],
                                 'Overall Monthly Costs': [weighted_sum_city_one, weighted_sum_city_two]})
    df_all_costs['Overall Monthly Costs'] = df_all_costs['Overall Monthly Costs'].apply(
        lambda x: "{:.2f}€".format(x))

    return df_all_costs


def get_difference_of_overall_costs(df_merged):
    city_one = 'Aachen'
    city_two = 'Berlin'
    selected_properties = get_selected_properties()
    df_copy = df_merged.copy(deep=True)
    df_copy_city_one = df_copy[['property', 'weight', city_one]]
    df_selected_city_one = df_copy_city_one.loc[df_copy_city_one['property'].isin(selected_properties)]
    df_selected_city_one['weighted_price'] = df_selected_city_one[city_one] * df_selected_city_one['weight']
    weighted_sum_city_one = round(df_selected_city_one['weighted_price'].sum(), 0)

    df_copy_city_two = df_copy[['property', 'weight', city_two]]
    df_selected_city_two = df_copy_city_two.loc[df_copy_city_two['property'].isin(selected_properties)]
    df_selected_city_two.fillna(1, inplace=True)
    df_selected_city_two['weighted_price'] = df_selected_city_two[city_two] * df_selected_city_two['weight']
    weighted_sum_city_two = round(df_selected_city_two['weighted_price'].sum(), 0)

    diff_in_costs = round(((weighted_sum_city_one - weighted_sum_city_two) / weighted_sum_city_one) * 100, 2)
    df_diff_in_costs = pd.DataFrame({f'Percentage Difference between {city_one} and {city_two}': [diff_in_costs]})
    df_diff_in_costs['diff'] = df_diff_in_costs[f'Percentage Difference between {city_one} and ' \
                                                f'{city_two}'].apply(lambda x: "{:.2f}%".format(x))

    return df_diff_in_costs


def prepare_data_for_piechart(df_merged):
    selected_properties = get_selected_properties()
    df_copy = df_merged.copy(deep=True)
    cities = ('Munich', 'Stuttgart', 'Karlsruhe', 'Heidelberg', 'Mannheim', 'Nuremberg', 'Darmstadt', 'Frankfurt',
              'Dresden', 'Leipzig', 'Berlin', 'Hanover', 'Bremen', 'Hamburg', 'Aachen', 'Bonn', 'Cologne', 'Dusseldorf',
              'Essen', 'Dortmund')
    df_copy_city_one = df_copy[['property', 'weight'] + list(cities)]
    df_selected_city_one = df_copy_city_one.loc[df_copy_city_one['property'].isin(selected_properties)]
    df_selected_city_one['category'] = float('nan')
    df_selected_city_one.loc[df_selected_city_one[
                                 'property'] == 'Meal for 2 People, Mid-range Restaurant, Three-course', 'category'] = \
        'Leisure (Sports, Cinema, Restaurants)'
    df_selected_city_one.loc[df_selected_city_one[
                                 'property'] == 'Fitness Club, Monthly Fee for 1 Adult', 'category'] = \
        'Leisure (Sports, Cinema, Restaurants)'
    df_selected_city_one.loc[df_selected_city_one[
                                 'property'] == 'Cinema, International Release, 1 Seat', 'category'] = \
        'Leisure (Sports, Cinema, Restaurants)'
    df_selected_city_one.loc[
        df_selected_city_one['property'] == 'Monthly Pass (Regular Price)', 'category'] = 'Transportation'
    df_selected_city_one.loc[df_selected_city_one[
                                 'property'] == 'Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)',
                             'category'] = 'Wifi and Mobile Phone'

    df_selected_city_one.loc[df_selected_city_one[
                                 'property'] == 'Apartment (1 bedroom) in City Centre', 'category'] = \
        'Accommodation (1 Bedroom in City Centre)'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Milk (regular), (1 liter)', 'category'] = 'Food'
    df_selected_city_one.loc[
        df_selected_city_one['property'] == 'Loaf of Fresh White Bread (500g)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Rice (white), (1kg)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Eggs (regular) (12)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Local Cheese (1kg)', 'category'] = 'Food'
    df_selected_city_one.loc[
        df_selected_city_one['property'] == 'Beef Round (1kg) (or Equivalent Back Leg Red Meat)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Apples (1kg)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Banana (1kg)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Oranges (1kg)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Tomato (1kg)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Potato (1kg)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Onion (1kg)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Lettuce (1 head)', 'category'] = 'Food'
    df_selected_city_one.loc[df_selected_city_one['property'] == 'Bottle of Wine (Mid-Range)', 'category'] = 'Food'

    return df_selected_city_one


def get_overall_monthly_cost_income(df_merged):
    city_list = ('Munich', 'Stuttgart', 'Karlsruhe', 'Heidelberg', 'Mannheim', 'Nuremberg', 'Darmstadt', 'Frankfurt',
                 'Dresden', 'Leipzig', 'Berlin', 'Hanover', 'Bremen', 'Hamburg', 'Aachen', 'Bonn', 'Cologne',
                 'Dusseldorf', 'Essen', 'Dortmund')
    selected_properties = get_selected_properties()
    df_copy = df_merged.copy(deep=True)
    df_all_costs = pd.DataFrame(columns=['City', 'Overall Monthly Costs'])

    for city in city_list:
        df_copy_city = df_copy[['property', 'weight', city]]
        df_selected_city = df_copy_city.loc[df_copy_city['property'].isin(selected_properties)]
        df_selected_city.fillna(1, inplace=True)
        df_selected_city['weighted_price'] = df_selected_city[city] * df_selected_city['weight']
        weighted_sum_city = round(df_selected_city['weighted_price'].sum(), 0)

        df_all_costs = df_all_costs._append({'City': city, 'Overall Monthly Costs': weighted_sum_city},
                                            ignore_index=True)

    df_gross_income = pd.read_csv('/Users/gjuresic/Desktop/python_projects/cost_of_living_german_cities/src/data/'
                                  'gross_income.csv', sep=';')
    df_all_costs_income = pd.merge(df_all_costs, df_gross_income, how='left', left_on=['City'], right_on=['city'])
    df_all_costs_income.drop('city', axis=1, inplace=True)
    df_all_costs_income.rename(columns={'gross_income': 'Gross Income'}, inplace=True)
    df_all_costs_income['Overall Monthly Costs'] = df_all_costs_income['Overall Monthly Costs'].astype(int)

    return df_all_costs_income
