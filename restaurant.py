# -*- coding: utf-8 -*-
##########################################################################################
#
#  Team:Tae Kim + Kevin Nguyen
#  Creator: Tae Kim
#
#  restaurant.py
#  April 22,2015
#
#  Restaurant Keeper that saves a list of restaurants that you like and view its information.
#  To add a restaurant, press 4 and copy and paste a yelp's link
#  To view your restaurant list, press 5, and it will display information including violations.
#
##########################################################################################

from lxml import html
import requests
import re
import sys
import json
import pandas as pd
import os.path
import requests.exceptions
import matplotlib
import warnings
warnings.filterwarnings("ignore")


from errorHandler import errorHandlerClass     #errorHandler.py
from OpenDataNYC import RestaurantData   #OpenNYCData

myRestaurantList={}    #global restaurant list
ratingList={}    #global rating list

def sourceReader(thisfile):
    '''
    Read a csv and return a dataframe after reindexing
    '''
    ratingList = pd.read_csv(thisfile,  usecols=['DBA', 'PHONE', 'BORO', 'ZIPCODE', 'CUISINE DESCRIPTION', 'VIOLATION DESCRIPTION','INSPECTION DATE', 'CRITICAL FLAG', 'SCORE', 'GRADE DATE', 'GRADE'],dtype='unicode').dropna()
    ratingList = ratingList.sort_index(by=["INSPECTION DATE"], ascending=True)
    ratingList.index =  xrange(len(ratingList))       #reindex because of removed rows
    return ratingList


def infoFinder(thisAddress):
    '''
    Parse the web for its information
    '''
    page = requests.get(thisAddress)
    tree = html.fromstring(page.text)       #get the html

    name_finder = tree.xpath('// h1[@itemprop="name"]/text()')
    try:        #name needs cleaning
        name_finder =  str(name_finder[0]).strip()
        name_finder = str(name_finder).encode('ascii', 'ignore')      #Due to encoding, "'" might throw an error  e.g. Wendy's
    except:
        thisError = sys.exc_info()[0]
        error = errorHandlerClass(thisError)
        error.errorHandlerFunction()

    street_finder = tree.xpath('//span[@itemprop="streetAddress"]/text()')   #parse
    city_finder = tree.xpath('//span[@itemprop="addressLocality"]/text()')
    price_finder = tree.xpath('//span[@itemprop="priceRange"]/text()')
    phone_finder = tree.xpath('//span[@itemprop="telephone"]/text()')
    phone_finder =  str(phone_finder[0]).strip()
    web_finder = tree.xpath('//div[@class="biz-website"]/a[@href]/text()')
    review_finder = tree.xpath('//li[@class="tab inline-block js-language-link selected"]/span[@class="count"]/text()')

    street_finder = "".join(street_finder)     #make it as string
    price_finder = "".join(price_finder)     #make it as string
    city_finder = "".join(city_finder)       #make it as string
    web_finder = "".join(web_finder)        #make it as string
    review_finder= "".join(review_finder)        #make it as string

    return name_finder, street_finder, city_finder, price_finder, phone_finder, web_finder, review_finder


def listBuilder():
    '''
    Compare the information from Yelp and join it with violation information from the city data
    and save it on json file
    These are some of links from Yelp (Top 10 restaurants in NYC according to Zagat)
    http://www.yelp.com/biz/le-bernardin-new-york
    http://www.yelp.com/biz/eleven-madison-park-new-york
    http://www.yelp.com/biz/daniel-new-york
    http://www.yelp.com/biz/sushi-yasuda-new-york
    http://www.yelp.com/biz/gramercy-tavern-new-york
    http://www.yelp.com/biz/peter-luger-steak-house-brooklyn
    http://www.yelp.com/biz/la-grenouille-new-york

    '''
    print "Please copy and paste the Yelp's link of the restaurant that you would like to add"
    try:
        print ("e.g. http://www.yelp.com/biz/bouley-new-york-2")
        thisLink = str(raw_input("---->  ")).replace(" ", "")

        name_finder, street_finder, city_finder, price_finder, phone_finder, web_finder, review_finder = infoFinder(thisLink)
        thisPhoneNum = re.sub("[()-]", '', phone_finder).replace(' ','')

        if os.path.exists("restaurant_list.csv")==True :        #in case if the user has used the program before to save a restaurant
                myRestaurantFromFile = pd.io.parsers.read_csv('restaurant_list.csv',sep="\t")   #read the file
                if myRestaurantFromFile['PHONE'].isin([int(thisPhoneNum)]).sum()>=1:  #previously stored
                    print "%s is already stored" %name_finder
                    askInput()       #data is already stored
                else:   #new entry
                    thisRating=ratingList[ratingList['PHONE'].isin([thisPhoneNum])]
                    if thisRating.empty:  #in case the phone number on Yelp can not be found in NYC Inspection data
                        thisRating=pd.DataFrame([{"DBA":"To be Updated", "BORO":"To be Updated", "ZIPCODE":"To be Updated", "PHONE":thisPhoneNum, "CUISINE DESCRIPTION":"To be Updated", "INSPECTION DATE":"To be Updated", "VIOLATION DESCRIPTION":"To be Updated", "CRITICAL FLAG":"To be Updated", "SCORE":"To be Updated", "GRADE":"To be Updated", "GRADE DATE":"To be Updated"}])
                    myRestaurantPD = pd.DataFrame([{"DBA_fromYelp":name_finder, "ADDRESS":street_finder, "CITY":city_finder, "PRICE":price_finder, "PHONE":thisPhoneNum, "WEB":web_finder, "REVIEW":review_finder}])
                    myRestaurantPD = pd.merge(myRestaurantPD, thisRating, on=["PHONE"], how='inner')
                    new = myRestaurantPD.append(myRestaurantFromFile, ignore_index=True, verify_integrity=False)
                    new.to_csv('restaurant_list.csv', sep='\t', encoding='utf-8', index=False)
                    print "%s is successfully added" %name_finder
        else:    #the user is new
                    thisRating=ratingList[ratingList['PHONE'].isin([thisPhoneNum])]
                    if thisRating.empty:  #in case the phone number on Yelp can not be found in NYC Inspection data
                         thisRating=pd.DataFrame([{"DBA":"To be Updated", "BORO":"To be Updated", "ZIPCODE":"To be Updated", "PHONE":thisPhoneNum, "CUISINE DESCRIPTION":"To be Updated", "INSPECTION DATE":"To be Updated", "VIOLATION DESCRIPTION":"To be Updated", "CRITICAL FLAG":"To be Updated", "SCORE":"To be Updated", "GRADE":"To be Updated", "GRADE DATE":"To be Updated"}])
                    myRestaurantPD = pd.DataFrame([{"DBA_fromYelp":name_finder, "ADDRESS":street_finder, "CITY":city_finder, "PRICE":price_finder, "PHONE":thisPhoneNum, "WEB":web_finder, "REVIEW":review_finder}])
                    myRestaurantPD = pd.merge(myRestaurantPD, thisRating, on=["PHONE"], how='inner')                                                    #the user is new
                    myRestaurantPD.to_csv('restaurant_list.csv', sep='\t', encoding='utf-8', index=False)
                    print "%s is successfully added" %name_finder
        myRestaurantPD.drop(myRestaurantPD.index[:])   #clear the dataframe
        askInput()
    except:
        thisError = sys.exc_info()[0]
        error = errorHandlerClass(thisError)
        error.errorHandlerFunction()

def listDelete():
    '''
    Delete the restaurant list file
    '''
    if os.path.exists("restaurant_list.csv")==True :
        os.remove('restaurant_list.csv')
        print "The list is successfully deleted"
    else:
        print "There is no file"
    askInput()


def optionPicker(thisOption):
    '''
    Input from a user and delegate the tasks
    '''
    if thisOption == 1:
        app_user.AssessPopularRestaurantsViolations()
        askInput()
    elif thisOption ==  2:
        #app_user.AssessBoroughViolations()
        app_user.RiskyHotSpots()
        askInput()
    elif thisOption ==  3:
        app_user.plotUserRestaurantGradeAndScore()
        askInput()
    elif thisOption ==  4:
        app_user.plotUserCuisineAndCriticalFlag()
        askInput()
    elif thisOption ==  5:
        app_user.AssessPopularCuisinesViolations()
        askInput()
    elif thisOption ==  6:
        listBuilder()
        infoFinder(thisOption)
    elif thisOption ==  7:
         quick_myRestaurantPrinter(myRestaurantList)
    elif thisOption ==  8:
        detail_myRestaurantPrinter(myRestaurantList)
    elif thisOption ==  9:
        listDelete()
    elif thisOption ==  0:
        print "Bye"
        sys.exit(1)
    else:
        print "Invalid option"


def quick_myRestaurantPrinter(myRestaurantList):
    '''
    Print out restaurant lists (short version)
    '''
    myRestaurantList =  pd.io.parsers.read_csv('restaurant_list.csv',sep="\t")
    df_unique = myRestaurantList.groupby("DBA_fromYelp").first()

    lenOfRestaurant=len(df_unique)
    print "There are %i restaurants in your Restaurant Keeper" %lenOfRestaurant
    print ""

    for i in xrange(lenOfRestaurant):
        print "-----------%i------------" %(i+1)
        print "Name: %s" %df_unique["DBA"].ix[i]
        print "Phone Number: %s" %df_unique["PHONE"].ix[i]
        print "Address: %s" %df_unique["ADDRESS"].ix[i]
        print "WEB: %s" %df_unique["WEB"].ix[i]
        print "PRICE: %s" %df_unique["PRICE"].ix[i]
        print "DESCRIPTION: %s" %df_unique["CUISINE DESCRIPTION"].ix[i]
        print ""
    askInput()


def detail_myRestaurantPrinter(myRestaurantList):
    '''
    Print out restaurant lists (all dataframe)
    '''
    myRestaurantList =  pd.io.parsers.read_csv('restaurant_list.csv',sep="\t")
    print myRestaurantList
    askInput()



def askInput():
  '''
  Print out options and receives an input.
  '''
  try:
    print ""
    print "*"*30
    print "Please select from following:"
    print "Type in 1 to See violations of popular restaurants in NYC"
    print "Type in 2 to View the Heatmap of NYC restaurants"
    print "Type in 3 to Explore the restaurant and the number of violations in your RestaurantKeeper"
    print "Type in 4 to Explore restaurants in your RestaurantKeeper grouped by types and the number of violations"
    print "Type in 5 to Explore violations of popular restaurants in NYC grouped by types"
    print "Type in 6 to Add a restaurant to your Restaurant Keeper"
    print "Type in 7 to Quick View of my Restaurant Keeper"
    print "Type in 8 to Full View of my Restaurant Keeper"
    print "Type in 9 to Reset my Restaurant Keeper"
    print "Type in 0 to Quit"
    print "*"*30
    print ""
    thisResponse = int(raw_input("What is your choice? "))
    optionPicker(thisResponse)     #optionPicker will delegate tasks
  except:
        thisError = sys.exc_info()[0]
        error = errorHandlerClass(thisError)
        error.errorHandlerFunction()

if __name__ == '__main__':
    thisfile ="DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
        #Due to the size of the file, I am not attaching the file to the github.
    if os.path.exists(thisfile)==True :
        ratingList = sourceReader(thisfile)
            # There are calling to initialize OpenDataNYC
        app_user = RestaurantData(ratingList)
        app_user.setUpNYCRestaurantData()
        app_user.getFlags()
        app_user.groupByCuisineAndBoro()
        app_user.createTop20List()
        app_user.filterTop20Cuisines()
        app_user.getGroupByCuisineAndBoro()
        app_user.UnstackDataset()
        app_user.createMeanSeries()
        app_user.getAverageScores()

        #Display options
        askInput()
    else:
        print "*"*30
        print "The required file is not in the folder, please check. "
        print "*"*30






