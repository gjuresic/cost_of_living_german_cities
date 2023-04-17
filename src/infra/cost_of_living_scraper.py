from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd


def scrape_data_from_website():
    list_of_cities = ['Munich', 'Stuttgart', 'Karlsruhe',
                      'Heidelberg', 'Mannheim', 'Nuremberg', 'Darmstadt', 'Frankfurt',
                      'Dresden', 'Leipzig', 'Berlin', 'Hanover', 'Bremen', 'Hamburg',
                      'Aachen', 'Bonn', 'Cologne', 'Dusseldorf', 'Essen', 'Dortmund']

    df_final = pd.DataFrame(columns=['city', 'category', 'property', 'price', 'currency', 'min_price',
                                     'max_price'])
    data_list = []

    for city in list_of_cities:
        url = f'https://www.numbeo.com/cost-of-living/in/{city}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', attrs={'class': 'data_wide_table new_bar_table'})
        rows = table.find_all('tr')

        batch_restaurant = np.arange(9)
        batch_markets = np.arange(9, 29)
        batch_transportation = np.arange(29, 38)
        batch_monthly_utilities = np.arange(38, 42)
        batch_sports_and_leisure = np.arange(42, 46)
        batch_childcare = np.arange(46, 49)
        batch_clothing_and_shoes = np.arange(49, 54)
        batch_rent_per_month = np.arange(54, 59)
        batch_buy_apartment_price = np.arange(59, 62)

        final_array = []

        # Loop over each row
        for row in batch_restaurant:
            new_row = []
            if row in [0, 9]:
                category = rows[row].text.split()
                category = category[0]
            elif row == 1:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:3])
                new_row = [concatenated_string] + property[3:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [2, 3]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:7])
                new_row = [concatenated_string] + property[7:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [4, 5]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:5])
                new_row = [concatenated_string] + property[5:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row == 6:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:2])
                new_row = [concatenated_string] + property[2:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [7, 8]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:4])
                new_row = [concatenated_string] + property[4:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        for row in batch_markets:
            new_row = []
            if row in [9]:
                category = rows[row].text.split()
                category = category[0]
            elif row in [12, 13, 14, 15, 23]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:3])
                new_row = [concatenated_string] + property[3:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [26, 27]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:5])
                new_row = [concatenated_string] + property[5:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [17, 18, 19, 20, 21, 22]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:2])
                new_row = [concatenated_string] + property[2:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [10, 24, 25, 28]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:4])
                new_row = [concatenated_string] + property[4:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [11]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:6])
                new_row = [concatenated_string] + property[6:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [16]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:9])
                new_row = [concatenated_string] + property[9:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        for row in batch_transportation:
            new_row = []
            if row in [29]:
                category = rows[row].text.split()
                category = category[0]
            elif row in [35]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:3])
                new_row = [concatenated_string] + property[3:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [34]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:5])
                new_row = [concatenated_string] + property[5:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [30, 31, 32, 33]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:4])
                new_row = [concatenated_string] + property[4:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [36, 37]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:10])
                new_row = [concatenated_string] + property[10:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        for row in batch_monthly_utilities:
            new_row = []
            if row in [38]:
                category = rows[row].text.split()
                category = ' '.join(category[:2])
            elif row in [41]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:8])
                new_row = [concatenated_string] + property[8:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [40]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:11])
                new_row = [concatenated_string] + property[11:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [39]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:9])
                new_row = [concatenated_string] + property[9:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        for row in batch_sports_and_leisure:
            new_row = []
            if row in [42]:
                category = rows[row].text.split()
                category = ' '.join(property[:3])
            elif row in [43, 44]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:7])
                new_row = [concatenated_string] + property[7:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [45]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:5])
                new_row = [concatenated_string] + property[5:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        for row in batch_childcare:
            new_row = []
            if row in [46]:
                category = rows[row].text.split()
                category = category[0]
            elif row in [47]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:10])
                new_row = [concatenated_string] + property[10:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [48]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:7])
                new_row = [concatenated_string] + property[7:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        for row in batch_clothing_and_shoes:
            new_row = []
            if row in [49]:
                category = rows[row].text.split()
                category = ' '.join(category[:3])
            elif row in [50]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:8])
                new_row = [concatenated_string] + property[8:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [51]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:10])
                new_row = [concatenated_string] + property[10:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            elif row in [52, 53]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:7])
                new_row = [concatenated_string] + property[7:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        for row in batch_rent_per_month:
            new_row = []
            if row in [54]:
                category = rows[row].text.split()
                category = ' '.join(category[:3])
            elif row in [55, 56, 57, 58]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:6])
                new_row = [concatenated_string] + property[6:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        for row in batch_buy_apartment_price:
            new_row = []
            if row in [59]:
                category = rows[row].text.split()
                category = ' '.join(property[:3])
            elif row in [60, 61]:
                property = rows[row].text.split()
                concatenated_string = ' '.join(property[:10])
                new_row = [concatenated_string] + property[10:-1]
                range = property[-1].split('-')
                new_row = new_row + range
                new_row.insert(0, category)
                new_row.insert(0, city)
            final_array.append(new_row)

        data_list += final_array
    df = pd.DataFrame(data_list, columns=['city', 'category', 'property', 'price', 'currency', 'min_price',
                                          'max_price'])
    df.drop_duplicates(inplace=True)
    df.dropna(subset=['city'], inplace=True)

    return df
