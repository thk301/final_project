# -*- coding: utf-8 -*-
###################################
#
#  Team:Tae Kim + Kevin Nguyen
#  Creator: Tae Kim 
#  Contributor: Kevin Nguyen
#
#  unittest_restaurant.py 
#  May 2nd,2015
#
#  1. testing input  1990 == 1990
#  2. testing csvReader
#  
###################################

import unittest
import restaurant as rt
import sys
import pandas as pd
from OpenDataNYC import RestaurantData

class restaurantTest(unittest.TestCase):

    def setUp(self):
        nyc_data_path = "DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
        user_list_path = pd.io.parsers.read_csv('restaurant_list.csv',sep="\t")
        self.RestaurantClass = RestaurantData(nyc_data_path)
        print "setUp"
    
    def testInfoFinder(self):
        '''
        Testing input
        '''
        thisAddress1="http://www.yelp.com/biz/bouley-new-york-2"
        self.assertEqual(rt.infoFinder(thisAddress1)[0:6], ('Bouley', '163 Duane St', 'New York', '$$$$', '(212) 964-2525', 'davidbouley.com'))  
        
        thisAddress2="http://www.yelp.com/biz/le-bernardin-new-york"
        self.assertEqual(rt.infoFinder(thisAddress2)[0:6], ('Le Bernardin', 'The Equitable Bldg155 W 51st St', 'New York', '$$$$', '(212) 554-1515', 'le-bernardin.com'))  
           
        
    def testCsvReader(self):
        '''
        Testing countryCsvReader function
        '''
        thisResult = rt.sourceReader('sample_data_for_unittesting.csv')
        phone = thisResult.PHONE.values
        violation = thisResult["VIOLATION DESCRIPTION"].values
        self.assertEqual(phone, '1234567890')    
        self.assertEqual(violation, 'test violation')  
          
    def testClassInstance(self):
         '''Test if RestaurantClass is an instance of the class.'''
         self.assertIsInstance(self.RestaurantClass, RestaurantData)

    def testInitialization(self):
        '''Test if global variables are created after initalization.'''
        self.assertIsNotNone(self.RestaurantClass.nyc_data)
        self.assertIsNone(self.RestaurantClass.clean_nyc_restaurant_data)

if __name__ == '__main__':
   unittest.main()
   
   