# -*- coding: utf-8 -*-
##########################################################################################
#
#  Team:Tae Kim + Kevin Nguyen
#  Creator: Kevin Nguyen
#
#  OpenDataNYC.py
#  May 10th,2015
#
##########################################################################################

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import sys



class RestaurantData(object):

    '''
    RestaurantData performs the analysis and visualization for the
    the program (both user input and overall NYC restaurant inspection
    data from 2013-01-02 to 2014-12-31).
    '''

    def __init__(self, clean_nyc_restaurant_data):

        """RestaurantData constructor.

        The constructor takes in two Panda DataFrames:

        1. New York City Restaurant Inspection Data: DOHMH_New_York_City_Restaurant_Inspection_Results.csv
        2. User selected and program scraped data from yelp.com and merged with New York City Restaurant Inspection Data

        Note:

        An empty global variable is created and then later changed when the method
        setUpNYCRestaurantData() is called.

        Attributes:
          nyc_data (Pandas DataFrame): `nyc_data` is a pandas dataframe that is used in this class to represent New City's overall resurants inspection data from 2013-01-02 to 2014-12-31.
          user_restaurant_list (Pandas DataFrame): 'user_restaurant_list' is data scraped from www.yelp.com and merged with DOHMH_New_York_City_Restaurant_Inspection_Results.csv data into a Pandas DataFrame.
          clean_nyc_restaurant_data (None): `clean_nyc_restaurant_data` will be used as a global variable for exploratory analysis after it is prepared with the method setUpNYCRestaurantData().

        """
        self.nyc_data = clean_nyc_restaurant_data
        self.clean_nyc_restaurant_data = None

    def setUpNYCRestaurantData(self):

        """Set up Restaurant Inspection Results data for analysis.

        Key Arguments Used:
          pd.replace(): Replace a cuisine description with a shorter label for plotting purposes.
          pd.astype("float"): Change data type for later computing with numpy.

        Return Attribute:
          - Clean dataset that we use for analysis

        """

        self.nyc_data = self.nyc_data.replace("Latin (Cuban, Dominican, Puerto Rican, South & Central American)", "Latin")
        self.nyc_data["SCORE"] = self.nyc_data["SCORE"].astype("float")
        self.nyc_data = self.nyc_data.replace("Missing", np.nan)
        self.clean_nyc_restaurant_data = self.nyc_data.replace("Not Yet Graded", np.nan)

    def getFlags(self):

        """Create indicator dummies based on "CRITICAL FLAG" for sorting and plotting purposes.

        Key Argument Used:
          pd.get_dummies()

        Return Attribute:
          - Data frame with two new columns: "Critical" and "Non-Critical"

        """
        self.clean_nyc_restaurant_data[["Critical", "Non-Critical"]] = pd.get_dummies(self.clean_nyc_restaurant_data["CRITICAL FLAG"])

    def groupByCuisineAndBoro(self):

        """Groupby "CUISINE DESCRIPTION" and "BORO" columns.

        Key Argument Used:
          pd.groupby()

        Return Attribute:
          - Pandas groupedby object

        """
        self.grouped_cuisine_and_boro = self.clean_nyc_restaurant_data.groupby(["CUISINE DESCRIPTION", "BORO"])

    def createTop20List(self):

        """Groupby "CUISINE DESCRIPTION" and "BORO" columns.

        Key Argument Used:
          pd.value_counts()[:20]: Get the top 20 graded cuisine descriptions
          pd.df.index.tolist():

        Return Attribute:
          - Data frame with the counts of the top 20 cuisine descriptions in New York City
          - List of restaurants names with the top 20 cuisine descriptions counts

        """
        top_20_cuisines = self.clean_nyc_restaurant_data["CUISINE DESCRIPTION"].value_counts()[:20]
        self.top_20_cuisines_list = top_20_cuisines.index.tolist()

    def filterTop20Cuisines(self):

        """Take restaurants only in the top 20 list.

        Key Argument Used:
          pd.dataframe.isin()

        Return Attribute:
          - Data frame (with all columns) of restaurants in the top 20 list.
        """

        self.top_20_cuisines_dataframe = self.clean_nyc_restaurant_data[self.clean_nyc_restaurant_data["CUISINE DESCRIPTION"].isin(self.top_20_cuisines_list)]

    def getGroupByCuisineAndBoro(self):

        """Generate groupby aggregation results for "CUISINE DESCRIPTION" and "BORO" with numpy.

        Key Argument Used:
          pd.DataFrame.agg([np.mean, np.count_nonzero, np.std])

        Return Attribute:
          - Data frame of the mean, std, and count of the restaurant scores grouped by "CUISINE DESCRIPTION" and "BORO".
        """
        self.cuisine_and_boro_group = pd.DataFrame(self.grouped_cuisine_and_boro["SCORE"].agg([np.mean, np.count_nonzero, np.std]))

    def UnstackDataset(self):

        """Unstack cuisine_and_boro_group for plotting purposes.

        Key Argument Used:
          grouped.unstack()

        Return Attribute:
          - Data frame of with the mean, std, and count of restaurant scores grouped by "CUISINE DESCRIPTION" and "BORO".
        """
        self.restaurant_cuisine_trends = self.cuisine_and_boro_group.unstack()

    def createMeanSeries(self):

        """Create a Pandas series with the mean scores.

        Key Argument Used:
          dataframe["mean"]

        Return Attribute:
          - A trend of restaurant scores (mean) in and pandas series
        """

        self.restaurant_trends_mean = self.restaurant_cuisine_trends["mean"]

    def getAverageScores(self):

        """Filter the restaurant trend series (mean) for the top 20 restaurants identified earlier.

        Key Argument Used:
          dataframe.index.isin()

        Return Attribute:
          - Our targeted restaurants with their mean scores
        """

        self.identified_dirty_restaurants_mean = self.restaurant_trends_mean[self.restaurant_trends_mean.index.isin(self.top_20_cuisines_list)]

    def AssessPopularCuisinesViolations(self):

        """Stacked bar chart of targeted cuisines and their count of violations.

        Key Argument Used:
          pd.crosstab.value_counts().plot()

        Return Attribute:
          - A pop up of the graph
          - A pdf graph saved as 'AssessPopularCuisinesViolations.pdf'
        """

        trends = pd.DataFrame(pd.crosstab(self.top_20_cuisines_dataframe["CUISINE DESCRIPTION"], self.top_20_cuisines_dataframe["CRITICAL FLAG"]))
        trends.sort(["Critical", "Not Critical"]).plot(kind="barh", stacked=True, figsize=(14,8))
        plt.ylabel("Cuisine \n")
        plt.xlabel('Number of Critical Flags')
        plt.title(r'Popular Restaurant Cuisines and Inspection Violations' )
        plt.tight_layout()  #This will generate UserWarning "UserWarning: tight_layout : falling back to Agg renderer" on Mac OS X
        plt.savefig('AssessPopularCuisinesViolations.pdf')
        plt.show()


    def AssessPopularRestaurantsViolations(self):

        """Stacked bar chart of targeted restaurants and their count of violations.

        Key Argument Used:
          pd.crosstab.value_counts().plot()

        Return Attribute:
          - A pop up of the graph
          - A pdf graph saved as "AssessPopularRestaurantsViolations.pdf".
        """

        trends = pd.DataFrame(pd.crosstab(self.clean_nyc_restaurant_data["DBA"], self.clean_nyc_restaurant_data["CRITICAL FLAG"]))
        trends.sort(["Critical", "Not Critical" ], ascending=False)[:20].plot(kind="barh", stacked=True, figsize=(14,8))
        plt.ylabel("Restaurant \n")
        plt.xlabel("Number of Critical Flags")
        plt.tick_params(labelsize=8)
        plt.title(r'Popular Restaurants and their Inspection Violations' )
        plt.tight_layout()    #This will generate UserWarning "UserWarning: tight_layout : falling back to Agg renderer" on Mac OS X
        plt.savefig('AssessPopularRestaurantsViolations.pdf')
        plt.show()

    def RiskyHotSpots(self):

        """Heatmap of NYC boroughs, targeted cuisines, and their mean violation scores.

        Return Attribute:
          - A pop up of the graph
          - A pdf graph saved as "Heatmap.pdf".
        """
        print self.identified_dirty_restaurants_mean
        fig, ax = plt.subplots()
        heatmap =ax.pcolor(self.identified_dirty_restaurants_mean, cmap=plt.cm.Blues)
        fig.colorbar(heatmap)
        plt.title("Check The Grades Before You Dine - Especially Ones With Darker Shades!")
        plt.xlabel("Borough")
        plt.ylabel("Cuisine")
        ax.set_xticks(np.arange(5) + 0.5, minor=False)
        ax.set_yticks(np.arange(20) + 0.5, minor=False)
        borou=[item for item in self.identified_dirty_restaurants_mean]
        cusine=['American ', 'Asian', 'Bakery', 'Cafe/Coffee/Tea', 'Caribbean', 'Chicken', 'Chinese', 'Delicatessen', 'Donuts', 'French',\
                 'Hamburgers', 'Indian','Italian', 'Japanese', 'Latin', 'Mexican', 'Pizza', 'Pizza/Italian', 'Sandwiches', 'Spanish']
        ax.set_xticklabels(borou, minor=False)
        ax.set_yticklabels(cusine, minor=False)
        plt.tick_params(labelsize=8)
        plt.tight_layout()   #This will generate UserWarning "UserWarning: tight_layout : falling back to Agg renderer" on Mac OS X
        plt.savefig("Heatmap.pdf")
        plt.show()


    def plotUserRestaurantGradeAndScore(self):

        """User graph of resturants and violations.

        Key Argument Used:
        pd.crosstab().sort().plot()

        Return Attribute:
          - A pop up of the graph
          - A pdf graph saved as "UserRestaurantAndScore.pdf".
        """
        user_restaurant_list = pd.io.parsers.read_csv('restaurant_list.csv',sep="\t")
        user_trends_restaurants = pd.DataFrame(pd.crosstab(user_restaurant_list["DBA"], user_restaurant_list["CRITICAL FLAG"]))
        user_trends_restaurants.sort(["Critical", "Not Critical" ], ascending=False).plot(kind="barh", stacked=True, figsize=(14,8))
        plt.ylabel("Restaurant \n")
        plt.xlabel("Number of Violations")
        plt.tick_params(labelsize=8)
        plt.title(r'User Restaurants and Inspection Violations' )
        plt.tight_layout()   #This will generate UserWarning "UserWarning: tight_layout : falling back to Agg renderer" on Mac OS X
        plt.savefig('UserRestaurantAndScore.pdf')
        plt.show()

    def plotUserCuisineAndCriticalFlag(self):

        """User graph of restaurants cuisine and inspection violations.

        Key Argument Used:
        pd.crosstab().sort().plot()

        Return Attribute:
          - A pop up of the graph
          - A pdf graph saved as "UserCuisinesAndScore.pdf".
        """
        user_restaurant_list = pd.io.parsers.read_csv('restaurant_list.csv',sep="\t")
        user_trends_cuisines = pd.DataFrame(pd.crosstab(user_restaurant_list["CUISINE DESCRIPTION"], user_restaurant_list["CRITICAL FLAG"]))
        user_trends_cuisines.sort(["Critical", "Not Critical"], ascending=False).plot(kind="barh", stacked=True, figsize=(14,8))
        plt.ylabel("Restaurant Cuisines \n")
        plt.xlabel("Number of Violations")
        plt.tick_params(labelsize=8)
        plt.title(r'User Restaurants Cuisines and Inspection Violations' )
        plt.tight_layout()    #This will generate UserWarning "UserWarning: tight_layout : falling back to Agg renderer" on Mac OS X
        plt.savefig('UserCuisinesAndScore.pdf')
        plt.show()
