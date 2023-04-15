# Your name: Sibora Berisha
# Your student id: 48866461
# Your email: sberisha@gmail.com
# List who you have worked with on this homework: Emma Moore

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
   # opening the database db usig conn and c similar to other hw 
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    c = conn.cursor()

    # selecting the name of each of the resaturant in the database
    c.execute("SELECT name FROM restaurants JOIN building")
    restaurant_names = c.fetchall()
    
    # initializing empty dict to hold the data for the restaurants
    restaurant_data = {}

    # getting the icategory building and rating for each restaurant from the db
    for name in restaurant_names:
        c.execute("SELECT category_id, building_id, rating FROM restaurants WHERE name=?", (name,))
        category, building, rating = c.fetchone()

    # add the info to the new dict 
    restaurant_data[name] = {"category_id": category, "building_id": building, "rating": rating}
    conn.close()
    return restaurant_data

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    # opening the database db usig conn and c similar to other hw
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("SELECT category_id, COUNT(*) FROM restaurants GROUP BY category ORDER BY COUNT(*) DESC")
    categories = []
    rest_number = []
    for row in c.fetchall():
        categories.append(row[0])
        rest_number.append(row[1])

    # Plot the bar graph
    fig, ax = plt.subplots()
    ax.barh(categories, rest_number, color='b')
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Restaurants")
    ax.set_title("Number of Restaurants per Category")
    ax.grip(True)
    plt.show()

    # Close 
    conn.close()

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    # opening the database db usig conn and c similar to other hw
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Get the restaurant names in the building, sorted by rating
    c.execute("SELECT name FROM restaurants WHERE building=? ORDER BY rating DESC", (building_num,))
    rows = c.fetchall()
    names_r = [row[0] for row in rows]

    # Close the database connection
    conn.close()

    return names_r

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """

#Try calling your functions here
def main():
    db = 'restaurants.db'
    
    # Load restaurant data and print the result
    restaurant_info = load_rest_data(db)
    print(restaurant_info)
    
    # Plot restaurant categories and print the result
    rest_categories = plot_rest_categories(db)
    print(rest_categories)
    
    # Find restaurants in a specific building and print the result
    rest_in_building = find_rest_in_building(db)
    print(rest_in_building)
 
class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
